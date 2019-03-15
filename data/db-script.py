import json
import psycopg2

def print_dict(dc, prefix="\t", depth=1):
    _prefix = prefix * depth

    for key, value in dc.items():
        if type(value) is dict:
            print(_prefix + key)
            print_dict(value, prefix, depth + 1)
        else:
            print(_prefix + key + ' : "' + str(value) + '"')

json_content = json.load(open('themes.txt', 'r'))

tb_name = "themes_theme"

conn = psycopg2.connect("host=localhost dbname=test user=andre password=Dodici12")
cursor = conn.cursor()

#create_query = "CREATE TABLE %s(name text, downloads integer, published boolean, authorAuth text, author text, alias_text_color text, alias_bg_color text, file_bg_color text, song_bg_color text, cmd_text_color text, default_bg_color text, apps_bg_color text, contact_bg_color text, contact_text_color text, song_text_color text, file_text_color text, default_text_color text, apps_text_color text, enabled boolean, transparent boolean, cmd_bg_color text, toolbar_color text, input_color text, enter_color text, time_color text, alias_content_color text, ram_color text, storage_color text, toolbar_bg text, battery_color_low text, app_uninstalled_color text, device_color text, output_color text, battery_color_medium text, overlay_color text, app_installed_color text, battery_color_high text, navigationbar_color text, statusbar_color text, bg_color text);" % (tb_name)

#cursor.execute(create_query)

columns = "battery_color_low, cmd_bg_color, storage_color, transparent_suggestions, ram_color, bg_color, cmd_text_color, alias_text_color, contact_text_color, author, contact_bg_color, enter_color, output_color, file_text_color, device_color, time_color, notes_color, downloads, apps_bg_color, song_bg_color, toolbar_color, alias_bg_color, name, battery_color_high, apps_text_color, song_text_color, input_color, toolbar_bg, file_bg_color, show_suggestions, battery_color_medium"

for _,theme in json_content.items():
    nulls = 0
    values = ""
    for key in columns.split(', '):
        try:
            value = theme[key]
        except:
            value = ""
            nulls += 1

        values = values + "'" + str(value) + "'" + ', '

    if nulls >= 10:
        print("skipped")
        continue

    values = values[:len(values)-2]

    query = "INSERT INTO %s (%s) VALUES (%s);" % (tb_name, columns, values)
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        break

conn.commit()

conn.close()
cursor.close()
