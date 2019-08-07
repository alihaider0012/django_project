from django.contrib import admin
from .models import UserProfile,Education,Accomplishment,Experience,Project,Skill,Post,File,following_list,Post_comment


admin.site.register(UserProfile)  #register a model in the admin panel for editing
admin.site.register(Education)  #register a model in the admin panel for editing
admin.site.register(Accomplishment)  #register a model in the admin panel for editing
admin.site.register(Experience)  #register a model in the admin panel for editing
admin.site.register(Project)  #register a model in the admin panel for editing
admin.site.register(Skill)  #register a model in the admin panel for editing
admin.site.register(Post)  #register a model in the admin panel for editing
admin.site.register(File)   #register a model in the admin panel for editing
admin.site.register(following_list) #register a model in the admin panel for editing
admin.site.register(Post_comment) #register a model in the admin panel for editing