from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.utils.safestring import mark_safe
from .models import Message,Chat,Chat_Participants,Chat_Messages,Group_Chat
from django.contrib.auth import get_user_model
from django.core import serializers
from nucircle.models import File
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
import json

User = get_user_model()

@login_required
def chatindex(request):
    return room(request, -1,True)


@login_required
def room(request, room_name,isFrontPage=False,errors=""):
    # print(errors)
    loggedInUser = request.user
    chatsandusers = Chat_Participants.objects.all().filter(user=loggedInUser)
    chats = []  
    
    currentChat = None
    currentChatFlag = False
    admin = False
    
    for x in chatsandusers:
        usersofthischat = Chat_Participants.objects.all().filter(chat=x.chat).exclude(user=loggedInUser)
        participants = []
        for i in usersofthischat:
            participants.append(i.user)
        
        # print(x.chat.admins.all())
        if loggedInUser in x.chat.admins.all():
            admin = True
        else:
            admin = False    

        
        if(x.chat.isSingleChat==False):
            groupChatDetails = Group_Chat.objects.all().filter(chat=x.chat).get()
            blockDictionary = {
                'chatContent':x.chat,
                'participants': participants ,
                'groupChatDetails':  groupChatDetails,
                'admin':admin   
            }
            # print("in for "+str(x.chat.id)+"->"+groupChatDetails.chatTitle)
        else:
            blockDictionary = {
                'chatContent':x.chat,
                'participants': participants ,
                'admin':admin  
            }
        
        if str(room_name) == str(x.chat.id):
            currentChat = blockDictionary
            currentChatFlag = True
        
        chats.append(blockDictionary)
    # print(uniqueParticipants)
    # print(chats)
    return render(request, 'chat/room.html', {
        'user':loggedInUser,
        'chats':chats,
        'currentChat':currentChat,
        'isFrontPage':mark_safe(json.dumps(isFrontPage)),
        'currentChatFlag':mark_safe(json.dumps(currentChatFlag)),
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'errors':mark_safe(json.dumps(errors))
    })
    

@login_required
def create_or_redirect_chat(request,userID):

    
    me = request.user
    
    if str(me.id) == str(userID):
        # print("yo yo")
        return room(request,-1,True)
        
    you = get_object_or_404(User,id = userID)
    chatsandusers = Chat_Participants.objects.all().filter(user=me)
    flag = False
    chatID = -1
    
    for x in chatsandusers:
        
        if x.chat.isSingleChat:
            getUser = Chat_Participants.objects.all().filter(chat=x.chat).exclude(user=me).get()
            if(you.username == getUser.user.username):
                flag = True
                chatID = x.chat.id
                break
        
        # usersofthischatcount = Chat_Participants.objects.all().filter(chat=x.chat).exclude(user=me).count()
        
        # if(usersofthischatcount == 1):
        #     getUser = Chat_Participants.objects.filter(chat=x.chat).exclude(user=me).get()
        #     if(you.username == getUser.user.username):
        #         flag = True
        #         chatID = x.chat.id
        #         break
          
    if(flag == False):     
        #CREATE NEW CHAT
        newChat = Chat.objects.create(
            
        ) 
        newChat.admins.add(me)
        newChat.admins.add(you)
        newChat.save()
        
        chatID = newChat.id
        Chat_Participants.objects.create(
            chat=newChat,
            user=me
        )
        
        Chat_Participants.objects.create(
            chat=newChat,
            user=you
        )
        chatID = newChat.id
        
    return room(request,chatID,False)

@login_required
def create_group_chat(request):    
    
    title = request.POST['title']
    usernames = request.POST['usernames']
    lastUser = request.POST['lastuser']
    
    usernameList = usernames.split(",")
    
    if lastUser != '':
        usernameList.append(lastUser)
        
    me = request.user   
    
    #CREATE CHAT
    createdChat = Chat.objects.create(
        isSingleChat= False
    )
    
    createdChat.admins.add(me)
    createdChat.save()
    #CREATE GROUP CHAT
    
    img = request.FILES.get('updated_group_image', False)
    print(img)
    if img:
        Group_Chat.objects.create(
            chatTitle=title,
            chat=createdChat,
            group_img=request.FILES['updated_group_image']
        )
    else:
        Group_Chat.objects.create(
            chatTitle=title,
            chat=createdChat,
            # group_img=request.FILES['updated_group_image']
        )

    #ADD PARTICIPANTS
    
    Chat_Participants.objects.create(
        chat=createdChat,
        user=me
    )
    
    errors = []
    
    for username in usernameList:
        try:
            instance = User.objects.get(username=username)
            Chat_Participants.objects.create(
                chat=createdChat,
                user=instance
            )
            # print (username+" created")
        except User.DoesNotExist:
            errors.append(username)
        
    # print(usernameList)
    # print(','.join(map(str, errors)) )
    return room(request,createdChat.id,False,','.join(map(str, errors)))


@login_required
def delete_chat(request,chatid):
    get_object_or_404(Chat,id=chatid).delete()   
    return chatindex(request)       
   
   
@login_required
def remove_group(request):
    chatid = request.POST['chatID']
    i = Chat_Participants.objects.all().filter(chat__id=chatid,user=request.user).get()  
    
    
    
    if request.user in i.chat.admins.all():
        i.chat.admins.remove(request.user)    
    
    i.delete()
    
    count = Chat_Participants.objects.all().filter(chat__id=chatid).count()
    # print(count)
    if count == 0:
        return delete_chat(request,chatid)
    
    return chatindex(request)       
    
@login_required    
def clear_chat(request):        
    chatid = request.POST['chatID']
   
    i = Chat_Participants.objects.all().filter(chat__id=chatid,user=request.user).get()  
    i.chat_cleared_at = datetime.datetime.now()
    i.save()
    # datai = serializers.serialize("json", User.objects.all())
    print("chat = "+chatid + " "+str(i.chat_cleared_at))
    
    return JsonResponse({"test":True})
    
    # return room(request,chatid,False,"")
    
@login_required   
def search_user(request): 
    query = request.POST['query']
    
    users = User.objects.all().filter(username__startswith=query).order_by('username').exclude(id=request.user.id)
    userlist = []
    
    for user in users:
        userlist.append({'username':user.username,'picture':user.userprofile.profile_image.url})
        
    # return JsonResponse({"users":serializers.serialize("json",userlist)})  
      
    return JsonResponse({"users":mark_safe(json.dumps(userlist))})      
       
       
@login_required       
def show_participants(request):       
    # print("in")
    chatid = request.POST['chatID']
    chat = get_object_or_404(Chat,id = chatid)
    chat_participants = Chat_Participants.objects.all().filter(chat__id=chatid).exclude(user__id=request.user.id)
    userlist = []
    
    for x in chat_participants:
        flag = False
        
        if x.user in x.chat.admins.all():
            flag=True
        
        dict =  {'username':x.user.username,'picture':x.user.userprofile.profile_image.url,'admin':flag}
        userlist.append(dict)
        
    # return JsonResponse({"users":serializers.serialize("json",userlist)})  
    # print(userlist)  
    return JsonResponse({"users":mark_safe(json.dumps(userlist))})  


@login_required  
def upload_file_to_chat(request):
    chatid = request.POST['chatID']
    title = request.POST['title']
    file = request.FILES.get('file', False)
    print(title)
    print(file)
    if file:
        createdFile = File.objects.create(
            title=title,
            user=request.user,
            file=file
        )
        myChat = Chat.objects.get(id = chatid)
        myChat.files.add(createdFile)
        myChat.save()
        
        
    
    return JsonResponse({})


@login_required
def upload_file_to_chat_from_myfiles(request):
    
    query = request.POST['query']
    result = File.objects.all().filter(user=request.user,title__icontains = query).order_by('title')
      
    return JsonResponse({"files":serializers.serialize("json", result)}) 


@login_required
def upload_file_to_chat_from_myfiles_button(request):
    pk = request.POST['fileID']
    chatID = request.POST['chatID']
    file = File.objects.get(pk=pk)
    chat = Chat.objects.get(id=chatID)
    flag = False
    if file in chat.files.all():
        flag = False


    else:
        flag = True
        chat.files.add(file)    
        
    return JsonResponse({'flag':mark_safe(json.dumps(flag))})
    

@login_required
def media_search(request):
    query = request.POST['query']
    chatID = request.POST['chatID']
    chat = Chat.objects.get(id=chatID)
    files = chat.files.all().filter(title__icontains = query)
    return JsonResponse({"files":serializers.serialize("json", files)})     


@login_required
def media_default(request):
    chatID = request.POST['chatID']
    chat = Chat.objects.get(id=chatID)
    files = chat.files.all()[:10]
    return JsonResponse({"files":serializers.serialize("json", files)})     


@login_required
def make_admin(request):
    participant_username = request.POST['participant_username']
    chatID = request.POST['chatID']

    Chat.objects.get(id=chatID).admins.add(User.objects.get(username=participant_username))
    return JsonResponse({'username':participant_username})

@login_required
def remove_participant(request):
    participant_username = request.POST['participant_username']
    chatID = request.POST['chatID']
    
    Chat_Participants.objects.get(chat__id = chatID,user__username=participant_username).delete()
    return JsonResponse({'username':participant_username})


@login_required
def setting_groupChat(request):
    title = request.POST['title']
    chatID = request.POST['chatID']
    img = request.FILES.get('file', False)
    
    chat = Group_Chat.objects.get(chat__id=chatID)
    chat.chatTitle = title
    if img:
        chat.group_img = img
        
    chat.save()
    
    return room(request,chatID,False)    
        
        
        
@login_required
def search_user_participant(request):

    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = User.objects.filter(username__startswith=q).exclude(id=request.user.id)
        results = []
        # print q
        for r in search_qs:
            results.append({"username":r.username,"picture":r.userprofile.profile_image.url})
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)  


@login_required
def add_participant(request):
    participant_username = request.POST['participant_username']
    chatID = request.POST['chatID']   
    
    participant = User.objects.get(username=participant_username)
    chat = Chat.objects.get(id=chatID)
    
    isPart = Chat_Participants.objects.filter(chat=chat,user=participant)
    
    if not isPart:
        Chat_Participants.objects.create(
            chat=chat,
            user=participant
        )
        return JsonResponse({'added':True,'username':participant_username,'picture':participant.userprofile.profile_image.url})   
    return JsonResponse({'added':False})
         