"""Consumers for chats."""

import json
from asgiref.sync import async_to_sync
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """Chat consumer."""

    async def connect(self):
        """Connect to the server."""
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Accept incoming connections
        await self.accept()

    async def disconnect(self, code):
        """Disconnect from the server."""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        """Receive a message from the server."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # Send the message to webSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.user.username,
                "datetime": now.isoformat(),
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        """Chat message."""
        # Send message to webSocket
        await self.send(text_data=json.dumps(event))
