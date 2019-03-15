from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('new_theme', views.new_theme),
    path('ajax/more_themes/<int:n>/<int:order_by>/<int:order_type>', views.more_themes, name='more_themes')
]
