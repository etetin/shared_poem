from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/add_symbol', consumers.Consumer),
]
