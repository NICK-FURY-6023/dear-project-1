
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync 
from django.contrib.auth.models import User
from chat.models import Thread, Message
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            self.close()
            return
            
        other_username = self.scope['url_route']['kwargs']['username'] 
        try:
            other_user = User.objects.get(username=other_username)
        except User.DoesNotExist:
            self.close()
            return
            
        self.thread_obj = Thread.objects.get_or_create_personal_thread(self.user, other_user)
        self.room_name = f'personal_thread_{self.thread_obj.id}'
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        
        self.accept()
        print(f'[{self.channel_name}] - {self.user.username} connected to chat with {other_username}')

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        print(f'[{self.channel_name}] - Disconnected')

    def receive(self, text_data):
        print(f'[{self.channel_name}] - Received message: {text_data}')
        
        # Store message in database
        self.store_message(text_data)
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': text_data,
                'username': self.user.username
            }
        )

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'text': event['message'],
            'username': event['username']
        }))
        print(f'[{self.channel_name}] - Message sent to client')
        
    def store_message(self, text):
        Message.objects.create(
            thread=self.thread_obj,
            sender=self.user,
            text=text
        )


class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(f'[{self.channel_name}] - Echo consumer connected')

    def disconnect(self, close_code):
        print(f'[{self.channel_name}] - Echo consumer disconnected')

    def receive(self, text_data):
        print(f'[{self.channel_name}] - Received: {text_data}')
        self.send(text_data=text_data)
