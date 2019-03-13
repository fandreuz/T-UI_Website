from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse

import datetime

from .models import Theme

import json

def index(request):
    template = loader.get_template('themes/index.html')

    now = datetime.datetime.now()
    dt = now.strftime("%Y-%m-%d")

    context = {
        "themes" : get_themes(20),
        "dt_string" : dt
    }

    return HttpResponse(template.render(context, request))

def new_theme(request):
    template = loader.get_template('themes/new_theme.html')

    now = datetime.datetime.now()
    dt = now.strftime("%Y-%m-%d")

    def_theme = Theme.objects.filter(author='tui-launcher').values()[0]
    adjust_colors(def_theme)

    context = {
        "default_theme" : def_theme,
        "dt_string" : dt
    }

    return HttpResponse(template.render(context, request))

# #rrggbbaa -> rrggbb (for jscolor)
def adjust_colors(theme):
    for k,v in theme.items():
        if type(v) == str and v.startswith('#') and len(v) == 9:
            theme[k] = v[1:7]

    return theme

def more_themes(request):
    how_much = request.GET.get('how_much', 20)
    data = {
        "themes" : get_themes(how_much)
    }
    return JsonResponse(data)

def get_themes(n):
    return list(Theme.objects.all())
