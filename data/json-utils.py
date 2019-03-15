import argparse
import json
import re

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# collapse the node if a non-ascii character is found
def check_node_asian(dc):
    for key in list(dc.keys()):
        value = dc[key]
        if not is_ascii(key):
            dc.pop(key)
        elif type(value) is dict:
            check_node_asian(value)

numbers = {
    '0' : 'Zero',
    '1' : 'One',
    '2' : 'Two',
    '3' : 'Three',
    '4' : 'Four',
    '5' : 'Five',
    '6' : 'Six',
    '7' : 'Seven',
    '8' : 'Eight',
    '9' : 'Nine'
}
def check_digits(dc, keep=[]):
    if keep == None:
        keep = []

    for key in list(dc.keys()):
        if key in keep:
            continue

        new_key = replace_leading_digits(key)
        if new_key != key:
            dc[new_key] = dc.pop(key)

        value = dc[new_key]
        if type(value) is dict:
            check_digits(value, keep)
        else:
            new_value = replace_leading_digits(str(value))
            dc[key] = new_value

def replace_leading_digits(st):
    ls = []
    match = re.search('^(\d)', st)
    while match:
        ls.append(match.group(1))
        st = st[1:]
        match = re.search('^(\d)', st)

    for key in reversed(ls):
        st = numbers[key] + st
    return st

def replace_rgb_with_hex(dc):
    for key,value in dc.items():
        if type(value) is dict:
            replace_rgb_with_hex(value)
        elif type(value) is str:
            new_value = rgb_to_hex(value)
            if new_value != None:
                dc[key] = new_value

def rgb_to_hex(st):
    match = re.search('rgb(?:a)?\((\d+),(?:\s)*(\d+),(?:\s)*(\d+)(?:,)?(?:\s)*(\d+(?:\.)?\d*)?\)', st)
    if match:
        r = match.group(1)
        g = match.group(2)
        b = match.group(3)

        if match.group(4) != None and len(match.group(4)):
            a = float(match.group(4)) * 255
        else:
            a = 255

        a = hex(int(a))[2:]
        if len(a) == 1:
            a = '0' + a

        r = hex(int(r))[2:]
        if len(r) == 1:
            r = '0' + r

        g = hex(int(g))[2:]
        if len(g) == 1:
            g = '0' + g

        b = hex(int(b))[2:]
        if len(b) == 1:
            b = '0' + b

        # #rgba

        return '#' + str(r) + str(g) + str(b) + str(a)

# build a model of the node (and its childs)
def get_django_model(node):
    st = ""

    for key, value in node.items():
        if type(value) is dict:
            st = st + "\n" + get_django_model(value)
        else:
            st = st + "\n" + key + " = models." + data_type_model(key,value)

    return st

boolean_values = ['True', 'true', 'False', 'false']
def data_type_model(key,value):
    if type(value) == int:
        return "IntegerField(default=%d)" % (value)
    elif type(value) == bool or value in boolean_values:
        return "BooleanField(default=%s)" % (str(value))
    else:
        return "TextField(default='%s')" % (str(value))

#######

def remove_symbols(dc, rm):
    for key, value in dc.items():
        if type(value) is dict:
            remove_symbols(value, rm)
        elif type(value) == str:
            new_value = re.sub('[%s]' % (rm), '', value)
            if new_value != value:
                dc[key] = new_value

#######

def rm_entries(dc, ls):
    for key in list(dc.keys()):
        if key in ls:
            dc.pop(key, None)
        elif type(dc[key]) is dict:
            rm_entries(dc[key], ls)

#######

def adjust_level(dc, max_level, c_level):
    for key in list(dc.keys()):
        value = dc[key]
        if type(value) is dict:
            if c_level == max_level - 1:
                # move up
                move_up(dc, value)
                dc.pop(key, None)
            else:
                adjust_level(value, max_level, c_level+1)

def move_up(dc_base, dc_from):
    for k,v in dc_from.items():
        if type(v) == dict:
            move_up(dc_base, v)
        else:
            dc_base[k] = v

#######

def get_sql_query(node):
    ls = fill_query(node)

    st = ""
    for i in ls:
        st = st + i[0] + " " + data_type_sql(i[0],i[1]) + ",\n"

    # remove trailing ,\n
    st = st[:len(st)-2]

    return st

def get_columns(node):
    ls = fill_query(node)

    st = ""
    for i in ls:
        st = st + i[0] + ", "

    # remove trailing ', '
    st = st[:len(st)-2]

    return st

def fill_query(node):
    ls = []

    for key, value in node.items():
        if type(value) is dict:
            ls.extend(fill_query(value))
        else:
            ls.append((key, value))

    return ls

def data_type_sql(key,value):
    if type(value) == int:
        return "integer"
    elif key == "pub_date":
        return "date"
    elif type(value) == bool or value in boolean_values:
        return "boolean"
    else:
        return "text"

######

def print_dict(dc, prefix="\t", depth=1):
    _prefix = prefix * depth

    for key, value in dc.items():
        if type(value) is dict:
            print(_prefix + key)
            print_dict(value, prefix, depth + 1)
        else:
            print(_prefix + key + ' : "' + str(value) + '"')

######

def rename(dc, old, new):
    for key in list(dc.keys()):
        try:
            ind = old.index(key)
            dc[new[ind]] = dc.pop(key, None)
        except:
            if type(dc[key]) is dict:
                rename(dc[key], old, new)

#Main

parser = argparse.ArgumentParser(description='Some JSON functions')
parser.add_argument('input_file', type=argparse.FileType('r'), help='A JSON file')
parser.add_argument('output_file', type=argparse.FileType('w'), nargs='?', help='An output file', default=open("output.txt", "w"))
parser.add_argument('-ra', action='store_true', help='Remove non-ASCII characters entries')
parser.add_argument('-rd', action='store_true', help='Replace digits with letters ("0" -> "Zero")')
parser.add_argument('-nc', action='store_true', help='Normalize the color format (rgb(...) -> #...)')
parser.add_argument('-rnm', '--rename', nargs='+', help='Rename key to (key1 key2 ... keyN new_key1 new_key2 ... new_keyN)')
parser.add_argument('-k', '--keep', nargs='+', help='Keep something')
parser.add_argument('-dm', nargs='*', help="Build a Django model from the input JSON file. You can provide a specific node ('-dm root child ...')")
parser.add_argument('-ds', nargs='*', help="Build a SQL query which creates a table for the specified JSON node. You can provide a specific node ('-ds root child ...')")
parser.add_argument('-cl', nargs='*', help="Build a list of columns inside the table created for the specified JSON node (see -ds). You can provide a specific node ('-ds root child ...')")
parser.add_argument('-rsy', nargs='+', help="Remove symbols from the values of the JSON file")
parser.add_argument('-rm', nargs='+', help="Remove entries")
parser.add_argument('-p', '--print', action='store_true', help='Print the result')
parser.add_argument('-c', '--count', action='store_true', help='Print the number of entries (before and after)')
parser.add_argument('-l', '--level', nargs=1, type=int, help="Set maximum number of levels in the JSON file")

args = parser.parse_args()
json_content = json.load(args.input_file)

if args.count:
    dc = json_content
    while(len(dc.keys()) <= 1):
        for i in dc.keys():
            dc = dc[i]
            break

    print("before: %d" % (len(dc.keys())))

args.output_file.truncate(0)

output = None

if args.ra:
    check_node_asian(json_content)
    output = json_content
if args.rd:
    check_digits(json_content, args.keep)
    output = json_content
if args.nc:
    replace_rgb_with_hex(json_content)
    output = json_content
if args.rsy != None:
    rm = ""
    for i in args.rsy:
        rm = rm + "\\%s" % (i)

    remove_symbols(json_content, rm)
    output = json_content
if args.rm != None:
    rm_entries(json_content, args.rm)
    output = json_content
if args.level != None:
    adjust_level(json_content, args.level[0], 0)
    output = json_content
if args.rename != None:
    old = args.rename[:len(args.rename)//2]
    new = args.rename[len(args.rename)//2:]

    rename(json_content, old, new)
    output = json_content

if args.dm != None:
    node = json_content
    for i in args.dm:
        node = node[i]
    model = get_django_model(node)
    output = model
if args.ds != None:
    node = json_content
    for i in args.ds:
        node = node[i]
    query = get_sql_query(node)
    output = query
if args.cl != None:
    node = json_content
    for i in args.cl:
        node = node[i]
    clmns = get_columns(node)
    output = clmns
if args.print:
    if type(output) == dict:
        print_dict(output)
    else:
        print(output)
else:
    if type(output) == dict:
        json.dump(output, args.output_file, sort_keys=True, indent=3, separators=(',', ': '))
    else:
        args.output_file.write(output)

if args.count:
    dc = json_content
    while(len(dc.keys()) <= 1):
        for i in dc.keys():
            dc = dc[i]
            break
    print("after: %d" % (len(dc.keys())))
