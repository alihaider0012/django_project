from django.contrib import admin

from .models import Message,Chat,Chat_Participants,Chat_Messages,Group_Chat

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(Chat_Participants)
admin.site.register(Chat_Messages)
admin.site.register(Group_Chat)