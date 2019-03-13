import re

#regex = '<div[^:]*:([^"]*)[^<]*<label[^>]*>([^<]*)[^d]*defaultvalue="([^"]*)"[^"]*"([^"]*)(?:[^v]|v(?!>))*'
#regex = '<span class="([^"]*)[^:]*:([^;]*)'
regex = '<div class="box ([^\s]*)\s([^"]*)[^:]*:\s*([^";]*);background-color:\s*([^;"]*)'

long_string = '''<div class="box file_bg_color file_text_color" style="color: rgba(0,0,0,1);background-color: rgba(3,169,244,1);">file</div>
<div class="box apps_bg_color apps_text_color" style="color: rgba(0,0,0,1);background-color: rgba(0,137,123,1);">apps</div>
<div class="box cmd_bg_color cmd_text_color" style="color: rgba(0,0,0,1);background-color: rgba(118,255,3,1);">cmd</div>
<div class="box song_bg_color song_text_color" style="color: rgba(0,0,0,1);background-color: rgba(238,255,65,1);">song</div>
<div class="box alias_bg_color alias_text_color" style="color: rgba(0,0,0,1);background-color:rgba(255,87,34,1);">alias</div>
<div class="box contact_bg_color contact_text_color" style="color: rgba(0,0,0,1);background-color: rgba(100,255,218,1);">contact</div>'''

'''for match in re.findall(regex, long_string):
    long_string = long_string.replace(match[0], "{{ default_theme.%s }}" % (match[1]), 1)
    long_string = long_string.replace(match[2], "{{ default_theme.%s }}" % (match[1]), 1)
    long_string = long_string.replace(match[3], "{{ default_theme.%s }}" % (match[1]), 1)'''

'''for match in re.findall(regex, long_string):
    long_string = long_string.replace(match[1], "{{ default_theme.%s }}" % (match[0]), 1)'''

for match in re.findall(regex, long_string):
    long_string = long_string.replace(match[2], "{{ default_theme.%s }}" % (match[1]), 1)
    long_string = long_string.replace(match[3], "{{ default_theme.%s }}" % (match[0]), 1)

print(long_string)
