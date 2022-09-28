from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/hi/", consumers.BoardConsumer.as_asgi()),
]