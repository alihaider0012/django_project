from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,get_list_or_404,redirect
from django.utils.safestring import mark_safe
from .models import Category,Comment,Forum_Post,Category_Request
from django.contrib.auth import get_user_model
from django.core import serializers
from django.urls import reverse
from . import urls
from nucircle.models import File
import datetime
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
import json


@login_required
def index(request):
    latest = Forum_Post.objects.order_by('-timestamp')[:3]
    return render(request, 'forum/index.html', {'latest':latest,'categories':Category.objects.all().order_by('title')})


@login_required
def createNewForum(request):
    return render(request, 'forum/create.html', {'categories':Category.objects.all().order_by('title')})


@login_required
def createNewPart1(request):
    title = request.POST['title']
    content = request.POST['content']
    categoriesID_list = request.POST.getlist('categories[]')

    created_forum = Forum_Post.objects.create(
        user=request.user,
        title= title,
        content = content
    )
    created_forum.categories.add(*categoriesID_list)
        
    created_forum.save()
    
    return JsonResponse({'id':mark_safe(json.dumps(created_forum.id))})    


@login_required
def createNewPart2(request):
    return redirect('forum:view_forum',forumid=14)


@login_required
def upload_file_to_forum(request):
    forumid = request.POST['forumID']
    title = request.POST['title']
    file = request.FILES.get('file', False)

    if file:
        createdFile = File.objects.create(
            title=title,
            user=request.user,
            file=file
        )
        myForum = Forum_Post.objects.get(id = forumid)
        myForum.files.add(createdFile)
        myForum.save()
        # lis = [createdFile.id,createdFile.file.url,createdFile.title] 
        return JsonResponse({})
    
    return JsonResponse({})


@login_required
def searchFromMyFilesBtn(request):
    pk = request.POST['fileID']
    forumid = request.POST['forumid']
    file = File.objects.get(pk=pk)
    forum = Forum_Post.objects.get(id=forumid)
    flag = False
    if file in forum.files.all():
        flag = False

    else:
        flag = True
        forum.files.add(file)    
        lis = [file.id,file.file.url,file.title]  
        return JsonResponse({'flag':mark_safe(json.dumps(flag))
                         ,'file':lis
                        })
    
    return JsonResponse({'flag':mark_safe(json.dumps(flag))})        


@login_required
def update_forum(request,forumid):
    flag = False
    try:
        forum = get_object_or_404(Forum_Post,id=forumid)
        flag = True
    except Forum_Post.DoesNotExist:
        flag = False
        
    if flag and forum.user == request.user:
        return render(request, 'forum/update.html', {
            'forum':forum,
            'categories':Category.objects.all().order_by('title')
        })        
    
    return redirect('forum:index')


@login_required
def update_text_stuff(request):
    title = request.POST['title']
    content = request.POST['content']
    categoriesID_list = request.POST.getlist('categories[]')
    forumid = request.POST.get('forumid',False)
    
    forum = Forum_Post.objects.get(id=forumid)
    forum.title = title
    forum.content = content
    forum.categories.clear()
    forum.categories.add(*categoriesID_list)

            
    forum.save()
    
    return JsonResponse({})    


@login_required
def delete_file_from_forum(request):
    forumid = request.POST['forumid']
    fileid =  request.POST['fileid']
    Forum_Post.objects.get(id=forumid).files.remove(File.objects.get(id=fileid))
    return JsonResponse({})    


@login_required
def delete_forum(request,forumid):
    
    try:
        forum = Forum_Post.objects.get(id=forumid)
        if forum.user == request.user:
            forum.delete()
            msg = 'Forum Deleted Successfully!'
        else:
            return redirect('forum:index')     

    except Forum_Post.DoesNotExist:
        msg = 'Forum does not exist'

    return redirect('forum:index')    


@login_required
def forum_search(request):
    query = request.POST['query']
    forums = Forum_Post.objects.all().filter(Q(title__icontains = query)|Q(user__username = query)).order_by('-timestamp')
    return JsonResponse({"forums":serializers.serialize("json", forums)}) 


@login_required
def forum_search_by_categories(request):
    
    categoriesID_list = request.POST.getlist('categories[]')
    print(categoriesID_list[0])
    forums = Forum_Post.objects.all().filter(categories__in = [categoriesID_list[0]]).distinct().order_by('-timestamp')
    print(forums)
    for cat in categoriesID_list:
        forums = forums & Forum_Post.objects.all().filter(categories__in = [cat]).distinct().order_by('-timestamp')
    
    return JsonResponse({"forums":serializers.serialize("json", forums)}) 


@login_required
def myposts(request):
    latest = Forum_Post.objects.filter(user = request.user).order_by('-timestamp')[:3]
    count = Forum_Post.objects.all().filter(user = request.user).count()
    return render(request, 'forum/myposts.html', {'latest':latest,'count':mark_safe(json.dumps(count)),'categories':Category.objects.all().order_by('title')})



@login_required
def forum_search_myposts(request):
    query = request.POST['query']
    forums = Forum_Post.objects.all().filter(user=request.user,title__icontains = query).order_by('-timestamp')
    return JsonResponse({"forums":serializers.serialize("json", forums)})


@login_required
def view_one_forum (request,forumid):
    print('in view forum')
    query = Forum_Post.objects.filter(id=forumid)
    
    if query.count() == 0:
        return redirect('forum:index')
    
    forum = query.get()
    return render(request, 'forum/post.html', {
        'forum':forum,
    }) 

 
@login_required
def like_dislike_comment(request):
    commentid = request.POST['commentid']
    comment = Comment.objects.get(id=commentid)
    flag = True
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        flag = False
    else:
        comment.likes.add(request.user)  
        
    return JsonResponse({'flag':mark_safe(json.dumps(flag))}) 


@login_required
def like_users(request):
    commentid = request.POST['commentid']
    comment = Comment.objects.get(id=commentid)
    
    lis = comment.likes.all().order_by('username')
    return JsonResponse({"users":serializers.serialize("json", lis)})


@login_required
def add_comment_to_forum(request):
    forumid = request.POST['forumid']
    text = request.POST['text']
    
    new_comment = Comment.objects.create(
        user = request.user,
        post = Forum_Post.objects.get(id=forumid),
        content = text
    )
    
    return JsonResponse({'id':mark_safe(json.dumps(new_comment.id))})
    
   
    
@login_required
def delete_comment(request):
    commentid = request.POST['commentid']
    comment = Comment.objects.get(id=commentid)    
    comment.delete()
    return JsonResponse({})


 
@login_required
def update_comment(request):
    
    commentid = request.POST['commentid']
    text = request.POST['text']
    comment = Comment.objects.get(id=commentid)    
    comment.content = text
    comment.save()
    return JsonResponse({})  


@login_required
def request_category(request):
    category = request.POST['category']
    
    flag = True
    
    if Category.objects.filter(title__iexact=category).exists():
        msg = 'Category already exists!'
        flag = False
    elif Category_Request.objects.filter(requested_category__iexact=category).exists():
        msg = 'Category already being processed!'
        flag = False
    else:
        Category_Request.objects.create(user=request.user,requested_category=category)
        msg = 'Category Requested Successfully!'

    return JsonResponse({'msg':msg,'flag':flag})  


@login_required
def accept_category_request(request):
    id = request.POST['requestid']
    request_obj = Category_Request.objects.get(id=id)
    
    Category.objects.create(title = request_obj.requested_category)
    
    request_obj.delete()
    
    return JsonResponse({})


@login_required
def delete_category_request(request):
    id = request.POST['requestid']
    request_obj = Category_Request.objects.get(id=id)  
    request_obj.delete() 
    return JsonResponse({})


@login_required
def forum_search_hospital_settings(request):
    # query = request.POST['query']
    userid = request.POST['userid']
    forums = Forum_Post.objects.all().filter(user__id = userid).order_by('-timestamp')
    return JsonResponse({"forums":serializers.serialize("json", forums)}) 


@login_required
def delete_forum_hospital_settings(request):
    forumid = request.POST['forumid']
    Forum_Post.objects.get(id=forumid).delete()
    return JsonResponse({})
