from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/add_symbol', views.add_symbol, name='add_symbol'),
]
