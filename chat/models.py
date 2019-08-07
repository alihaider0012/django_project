from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from nucircle.models import File
from django.db import models

User = get_user_model()

def group_directory_path(instance, filename):
    return f'group_{instance.chat.id}/{filename}'

class Message(models.Model):
    author = models.ForeignKey(
        User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.author.username+" ==> "+self.content)
    
    
    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]
    
    
class Chat(models.Model):
    isSingleChat = models.BooleanField(default=True)
    admins = models.ManyToManyField(
        User, related_name='admins')
    files = models.ManyToManyField(
        File, related_name='files')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(str(self.id) + " "+str(self.isSingleChat))   
    

    

    
        
class Chat_Participants(models.Model):
    user = models.ForeignKey(
        User, related_name='user',on_delete=models.CASCADE)
    chat = models.ForeignKey(
        Chat, related_name='chat_participant',on_delete=models.CASCADE)
    chat_cleared_at = models.DateTimeField(default=datetime.datetime.now())
    
    def __str__(self):
        return (self.user.username+ " <-> "+str(self.chat.id))
    
    
class Chat_Messages(models.Model):
    chat = models.ForeignKey(
        Chat, related_name='chat_message',on_delete=models.CASCADE)  
    message = models.ForeignKey(
        Message, related_name='message',on_delete=models.CASCADE)  
    # msg_created_at = models.DateTimeField(default=datetime.datetime.now())
    
    
    def __str__(self):
        return (str(self.chat.id)+ " messaged "+self.message.content)
    

        
class Group_Chat (models.Model):
    chat = models.ForeignKey(
        Chat, related_name='chat_group',on_delete=models.CASCADE)  
    chatTitle = models.CharField(max_length = 100,default='NO-NAME')
    group_img = models.ImageField(upload_to=group_directory_path, default="no_image.png", blank=True, null=True) 
    
    def __str__(self):
        return str(self.chat.id) +" <==> "+ self.chatTitle   