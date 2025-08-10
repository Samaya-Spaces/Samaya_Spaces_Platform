# chat/routing.py

from django.urls import re_path
from . import consumers

# This variable MUST be named exactly 'websocket_urlpatterns'
# because asgi.py is looking for it.
websocket_urlpatterns = [
    # This regular expression matches the URL that your JavaScript is trying to connect to.
    # It looks for URLs that start with 'ws/chat/', followed by a number (the ID),
    # and a final slash.
    re_path(r'ws/chat/(?P<conversation_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]