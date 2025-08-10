# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope['user']

        print(f"--- [CONNECT] User '{self.user.username}' trying to connect to group '{self.conversation_group_name}'")

        if self.user.is_authenticated and await self.is_participant():
            await self.channel_layer.group_add(
                self.conversation_group_name, self.channel_name
            )
            await self.accept()
            print(f"--- [SUCCESS] User '{self.user.username}' connected successfully.")
        else:
            await self.close()
            print(f"--- [FAIL] User '{self.user.username}' connection denied.")

    async def disconnect(self, close_code):
        print(f"--- [DISCONNECT] User '{self.user.username}' disconnected from group '{self.conversation_group_name}'")
        await self.channel_layer.group_discard(
            self.conversation_group_name, self.channel_name
        )

    # This is called when we receive a message FROM the browser
    async def receive(self, text_data):
        print(f"--- [RECEIVE] Received message from '{self.user.username}'")
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        
        if not message_content.strip(): return

        await self.save_message(message_content)
        
        # This sends the message TO the channel layer (Redis)
        print(f"--- [BROADCASTING] Sending message to group '{self.conversation_group_name}'")
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message', # This specifies which method to call on the receiving consumers
                'message': message_content,
                'username': self.user.username
            }
        )
        print("--- [BROADCAST] Message sent to group.")

    # This is called when this consumer receives a message FROM the group
    async def chat_message(self, event):
        print(f"--- [GROUP MESSAGE] Consumer for user '{self.user.username}' received a message from the group.")
        message = event['message']
        username = event['username']

        # This sends the message back down the WebSocket TO the browser
        print(f"--- [SENDING] Sending message to '{self.user.username}'s browser.")
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
        print("--- [SENT] Message sent to browser.")

    # --- Database Helper Methods ---
    @database_sync_to_async
    def is_participant(self):
        try:
            conversation = Conversation.objects.get(pk=self.conversation_id)
            return self.user in conversation.participants.all()
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, message_content):
        conversation = Conversation.objects.get(pk=self.conversation_id)
        Message.objects.create(
            conversation=conversation, author=self.user, content=message_content
        )