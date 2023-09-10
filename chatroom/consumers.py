import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import datetime
from .models import Message, Chatroom


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_name = f'chat_{self.chat_id}'
        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(
            self.chat_name,
            self.channel_name
        )

        if self.user.is_anonymous and not Chatroom.objects.get(id=self.chat_id).is_anonymous:
            self.close()

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json['load_msg']:
            msgs = Message.objects.filter(id__lt=int(text_data_json['before_id']),
                                          chatroom_id=self.chat_id).order_by('-id')[:5]

            self.send(text_data=json.dumps({
                'type': 'load_msg',
                'message': [{"id": msg.id,
                             "msg": f'{msg.created_at:%Y-%m-%d %H:%M:%S} {msg.createc_by if msg.createc_by else "AnonymousUser"}: {msg.content}'}
                            for msg in msgs],
            }))
        else:
            message = text_data_json['message']

            if self.user.is_anonymous:
                msg = Message.objects.create(content=message, chatroom_id=self.chat_id)
            else:
                msg = Message.objects.create(content=message, chatroom_id=self.chat_id, createc_by=self.user)

            async_to_sync(self.channel_layer.group_send)(
                self.chat_name,
                {
                    'type': 'chat_message',
                    'message': msg,
                    'msgId': msg.id,
                }
            )

    def chat_message(self, event):
        message = event['message']
        datetime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.send(text_data=json.dumps({
            'msg_type': event['type'],
            'message': f'{datetime_str} {"AnonymousUser" if message.chatroom.is_anonymous else message.createc_by}: {message.content}',
            'msgId': event['msgId']
        }))
