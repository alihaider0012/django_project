from django.urls import path, include,re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'forum'

urlpatterns = [
    path(r'',views.index, name='index'),
    url(r'^forum_search/ajax$',views.forum_search, name='forum_search'),
    url(r'^forum_search_by_categories/ajax$',views.forum_search_by_categories, name='forum_search_by_categories'),
    
    #CRUD
    url(r'^create/$', views.createNewForum, name='createNewForum'),
    url(r'^create/newPart1$', views.createNewPart1, name='createNewPart1'),
    url(r'^create/newPart2$', views.createNewPart2, name='createNewPart2'),
    url(r'^create/uploadFile/new/', views.upload_file_to_forum, name='upload_file_to_forum'),
    url(r'^ajax/searchFromMyFilesBtn$', views.searchFromMyFilesBtn, name='searchFromMyFilesBtn'),
    
    url(r'^(?P<forumid>[0-9]+)/$',views.view_one_forum, name='view_forum'),
    url(r'^(?P<forumid>[0-9]+)/update/$',views.update_forum, name='update_forum'),
    url(r'^update_text_stuff/ajax$',views.update_text_stuff, name='update_text_stuff'),
    url(r'^delete_file_from_forum/$',views.delete_file_from_forum, name='delete_file_from_forum'),
    url(r'^(?P<forumid>[0-9]+)/delete/$',views.delete_forum, name='delete_forum'),
    url(r'^like_dislike_comment/ajax$',views.like_dislike_comment, name='like_dislike_comment'),
    
    url(r'^like_users/ajax$',views.like_users, name='like_users'),
    url(r'^add_comment_to_forum/ajax$',views.add_comment_to_forum, name='add_comment_to_forum'),
    url(r'^delete_comment/ajax$',views.delete_comment, name='delete_comment'),
    url(r'^update_comment/ajax$',views.update_comment, name='update_comment'),
    
    # forum_search_myposts
     url(r'^forum_search_myposts/ajax$',views.forum_search_myposts, name='forum_search_myposts'),
    url(r'^myposts/$', views.myposts, name='myposts'),
    url(r'^request_category/ajax$', views.request_category, name='request_category'),
    url(r'^accept_category_request/$', views.accept_category_request, name='accept_category_request'),
    url(r'^delete_category_request/$', views.delete_category_request, name='delete_category_request'),
    url(r'^forum_search_hospital_settings/ajax$',views.forum_search_hospital_settings, name='forum_search_hospital_settings'),
    url(r'^delete_forum_hospital_settings/ajax$',views.delete_forum_hospital_settings, name='delete_forum_hospital_settings'),
] 