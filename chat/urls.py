# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    # This is the new URL for the inbox page
    path('', views.inbox_view, name='inbox'),
    
    # This is the existing URL for a specific chat room
    path('<int:conversation_id>/', views.chat_room_view, name='room'),
]