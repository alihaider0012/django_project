from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404, get_list_or_404
from channels.generic.websocket import WebsocketConsumer
import datetime
import json
from .models import Message,Chat,Chat_Participants,Chat_Messages
User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print(data)

        # v = Chat_Participants.objects.all().filter(chat__id=data['chatID'],user__username=data['username']).get()
        # messages =Chat_Messages.objects.all().filter(chat__id = data['chatID']).exclude(message__timestamp__lt=v.chat_cleared_at).order_by('message__timestamp')
        messages =Chat_Messages.objects.all().filter(chat = get_object_or_404(Chat,pk=data['chatID'])).order_by('message__timestamp')
        # print(v.chat_cleared_at)
        # print(messages)
        msgs = []
        allmessagesCount = messages.count()
        messageCount = data['messageCount']
        flag = False
        if messageCount >= allmessagesCount:
            xc = messageCount-allmessagesCount
            messageCount = allmessagesCount
            flag=True
            for x in messages[0:(allmessagesCount%10)]:
                msgs.append(x.message)
        else:
            for x in messages[allmessagesCount-messageCount:allmessagesCount-messageCount+10]:
                msgs.append(x.message)


        content = {
            'command': 'messages',
            'messages': self.messages_to_json(msgs),
            'flagForVisibility':flag
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message1 = Message.objects.create(
            author=author_user, 
            content=data['message'])
        Chat_Messages.objects.create(
            chat = get_object_or_404(Chat, pk=data['chatID']),
            message = message1
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message1)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        

    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))