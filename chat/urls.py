from django.urls import path, include,re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
app_name = 'chat'
from . import views
urlpatterns = [
    path(r'',views.chatindex, name='index'),
    re_path(r'^(?P<room_name>[^/]+)/$',views.room, name='room'),
    url(r'^create_or_redirect_chat/(?P<userID>[0-9]+)/$', views.create_or_redirect_chat, name='create_or_redirect_chat'),
    url(r'create_group_chat/new/', views.create_group_chat, name='create_group_chat'),
    # url(r'^delete_chat/(?P<chatid>[0-9]+)/$', delete_chat, name='delete_chat'),
    url(r'^remove_group/removeMe/', views.remove_group, name='remove_group'),
    url(r'^clear_chat/clearThis/', views.clear_chat, name='clear_chat'),
    url(r'^search/user/', views.search_user, name='search_user'),
    url(r'^showParticipants/show/', views.show_participants, name='show_participants'),
    url(r'^upload/new/', views.upload_file_to_chat, name='upload_file_to_chat'),
    url(r'^upload/existing/', views.upload_file_to_chat_from_myfiles, name='upload_file_to_chat_from_myfiles'),
    url(r'^upload/btn/', views.upload_file_to_chat_from_myfiles_button, name='upload_file_to_chat_from_myfiles_button'),
    url(r'^media/search/', views.media_search, name='media_search'),
    url(r'^media/default/', views.media_default, name='media_default'),
    url(r'^make_admin/ajax/', views.make_admin, name='make_admin'),
    url(r'^remove_participant/ajax/', views.remove_participant, name='remove_participant'),
    url(r'^settings/group/', views.setting_groupChat, name='setting_groupChat'),
    url(r'^search/user_participant/', views.search_user_participant, name='search_user_participant'),
    url(r'^add_participant/add/', views.add_participant, name='add_participant'),
] 
