import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Thread, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group_name = f'chat_{self.thread_id}'

        # Join thread group
        await self.channel_layer.group_add(
            self.thread_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave thread group
        await self.channel_layer.group_discard(
            self.thread_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        attachment_url = text_data_json.get('attachment_url', None)
        
        sender = await self.get_user(sender_id)
        thread = await self.get_thread(self.thread_id)
    
    if sender and thread:
        await self.create_message(thread, sender, message, attachment_url)
        
        await self.channel_layer.group_send(
            self.thread_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'sender_username': sender.username,
                'attachment_url': attachment_url,
                'is_image': attachment_url and any(ext in attachment_url.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif'])
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_username = event['sender_username']
        attachment_url = event.get('attachment_url')
        is_image = event.get('is_image', False)
    
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender_username,
            'attachment_url': attachment_url,
            'is_image': is_image
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_thread(self, thread_id):
        try:
            return Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, thread, sender, text):
        Message.objects.create(thread=thread, sender=sender, text=text)