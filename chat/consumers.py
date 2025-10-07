
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync 
from django.contrib.auth.models import User
from chat.models import Thread, Message
from lxfpro.mongo_models import MongoChatMessage, MongoActivityLog
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
        # Save to SQLite (existing Django ORM)
        Message.objects.create(
            thread=self.thread_obj,
            sender=self.user,
            text=text
        )
        
        # Save to MongoDB Atlas for analytics and notifications
        try:
            # Get receiver ID (the other user in the thread)
            receiver = self.thread_obj.first_person if self.thread_obj.second_person == self.user else self.thread_obj.second_person
            
            MongoChatMessage.create(
                sender_id=self.user.id,
                receiver_id=receiver.id,
                message=text,
                thread_id=str(self.thread_obj.id)
            )
            
            # Log activity for notification system
            MongoActivityLog.log(
                user_id=self.user.id,
                action='websocket_message',
                details={
                    'to_user': receiver.username,
                    'thread_id': str(self.thread_obj.id),
                    'preview': text[:50]
                }
            )
            
            print(f'✅ Message saved to MongoDB: {self.user.username} → {receiver.username}')
        except Exception as e:
            print(f'❌ MongoDB save error: {e}')


class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(f'[{self.channel_name}] - Echo consumer connected')

    def disconnect(self, close_code):
        print(f'[{self.channel_name}] - Echo consumer disconnected')

    def receive(self, text_data):
        print(f'[{self.channel_name}] - Received: {text_data}')
        self.send(text_data=text_data)
