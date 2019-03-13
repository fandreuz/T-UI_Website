from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('new_theme', views.new_theme),
    path('/ajax/more_themes/', views.more_themes, name='more_themes')
]
