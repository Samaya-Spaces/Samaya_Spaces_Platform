from django.urls import re_path
# We will create the consumer in the next part of the lesson
# from . import consumers 

# For now, we'll leave the urlpatterns empty. We'll fill this in next.
websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]