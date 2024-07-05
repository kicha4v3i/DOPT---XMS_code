
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/ticket/startticket/(?P<room_name>[^/]+)/$', consumers.ChatRoomConsumer.as_asgi()),
]
