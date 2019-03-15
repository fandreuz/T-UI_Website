from django.db import models

class Theme(models.Model):
    #theme
    input_color = models.TextField(default='#00ff00ff')
    toolbar_color = models.TextField(default='#ff0000ff')
    bg_color = models.TextField(default='#000000ff')
    storage_color = models.TextField(default='#9c27b0ff')
    output_color = models.TextField(default='#ffffffff')
    enter_color = models.TextField(default='#ffffffff')
    battery_color_low = models.TextField(default='#ff5722ff')
    battery_color_medium = models.TextField(default='#ffeb3bff')
    battery_color_high = models.TextField(default='#4caf50ff')
    ram_color = models.TextField(default='#f44336ff')
    time_color = models.TextField(default='#03a9f4ff')
    device_color = models.TextField(default='#ff9800ff')
    toolbar_bg = models.TextField(default='#00000000')
    notes_color = models.TextField(default='#8BC34A')

    #suggestions
    alias_bg_color = models.TextField(default='#ff5722ff')
    apps_text_color = models.TextField(default='#000000ff')
    show_suggestions = models.BooleanField(default=True)
    file_text_color = models.TextField(default='#000000ff')
    alias_text_color = models.TextField(default='#000000ff')
    cmd_text_color = models.TextField(default='#000000ff')
    cmd_bg_color = models.TextField(default='#76ff03ff')
    song_bg_color = models.TextField(default='#eeff41ff')
    transparent_suggestions = models.BooleanField(default=False)
    apps_bg_color = models.TextField(default='#00897bff')
    song_text_color = models.TextField(default='#000000ff')
    file_bg_color = models.TextField(default='#03a9f4ff')
    contact_text_color = models.TextField(default='#000000ff')
    contact_bg_color = models.TextField(default='#64ffdaff')

    #other
    author = models.TextField(default='tui-launcher')
    downloads = models.IntegerField(default=0)
    name = models.TextField()
