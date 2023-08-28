"""Consumers for chats."""

import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    """Chat consumer."""

    def connect(self):
        """Connect to the server."""
        # Accept incoming connections
        self.accept()

    def disconnect(self, code):
        """Disconnect from the server."""

    # Receive message from WebSocket
    def receive(self, text_data):
        """Receive a message from the server."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send the message to webSocket
        self.send(text_data=json.dumps({"message": message}))
