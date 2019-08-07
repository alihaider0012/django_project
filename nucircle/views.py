from django.http import Http404
from django.http import HttpResponse
from django.template import loader 
from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib import auth
from django.contrib.auth.models import User
import openpyxl
import re
import json
import csv,io
from django.utils.safestring import mark_safe
from forum.models import Category_Request
from .models import *
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser,JSONParser, MultiPartParser, FormParser
from rest_framework import status
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'nucircle/index.html')
    else:
        return redirect('nucircle:newsfeed')

def signup(request):
    if request.method == 'POST':
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        # username = request.POST['username'] 
        email = request.POST['email']
        
        if User.objects.all().filter(email=email).exists():
            return JsonResponse({'message':'User with same email already exists!'})
        
        hcode = get_hospital_code(request.user.username)
        
        try:
            latest_user = User.objects.all().filter(username__startswith=hcode+'-u').latest('id')
            count = int(latest_user.username.split('-u')[1])
        except User.DoesNotExist:
            count = 0
        
        username = hcode+'-u'+str(count+1)
        isValid, message = FormValidator.signup_validation(username, email, password_1, password_2)        
        if not isValid: 
            return JsonResponse({'message':message['error']})
        else:
            user = User.objects.create_user(username=username, email=email, password=password_1)  
            user.userprofile.update_fields(location=request.user.userprofile.location)
            send_email(request,email,username,password_1,False)
            return JsonResponse({'message':'User created successfully\nUsername: '+username+'\nPassword:'+password_1})
    else:
        return render(request, 'nucircle/index.html')     
    
    
def get_hospital_code(username):
    return username.split('-')[0]    

def login(request):
    if request.user.is_authenticated:
        return redirect('nucircle:newsfeed')
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password']
        isValid, message = FormValidator.login_validation(username, password)        
        if not isValid:   
            return render(request, 'nucircle/index.html', message)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if password == 'default123':
                return redirect(reverse("nucircle:change_password"))
            return redirect(reverse("nucircle:newsfeed"))
        else:
            return render(request, 'nucircle/index.html', { 'error_field': 'password', 'error_form' : 'login',
                                                            'error': 'Wrong password', 
                                                            'username' : username,})
    else:
        return render(request, 'nucircle/index.html')
    
@login_required
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect(reverse("nucircle:index"))
    else:
        return redirect('nucircle:profile')    

@login_required
def profile(request, user_id = -1, error=''):
   
    if int(user_id) == int(request.user.id) or user_id == -1:
        return render(request, 'nucircle/profile.html', {   'user': request.user,
                                                            'online_user': request.user,
                                                            'isOwner': True,
                                                            'education': Education.objects.all().filter(user=request.user.id),
                                                            'accomplishment': Accomplishment.objects.all().filter(user=request.user.id),
                                                            'experience': Experience.objects.all().filter(user=request.user.id),    
                                                            'skill': Skill.objects.all().filter(user=request.user.id),    
                                                            # 'interest': Interest.objects.all().filter(user=request.user.id),    
                                                            'project': Project.objects.all().filter(user=request.user.id)})    

    else:
        user = get_object_or_404(User, pk=user_id)
        flag = True
        list = following_list.objects.get(user=request.user)
        if not user in list.following.all():
            flag = False
        return render(request, 'nucircle/profile.html', {   'user': user,
                                                            'online_user': request.user,
                                                            'isOwner': False,
                                                            # 'isRequestReceived': bool(DB_Helper.checkRequestReceived(request.user.id, user_id)),      
                                                            'error': error,
                                                            'isFollow':flag,
                                                            # 'isRequestSent': bool(DB_Helper.checkRequestSend(request.user.id, user_id)),     
                                                            # 'isFriend': bool(DB_Helper.checkFriendship(request.user.id, user_id)),    
                                                            'education': Education.objects.all().filter(user=user),
                                                            'accomplishment': Accomplishment.objects.all().filter(user=user),
                                                            'experience': Experience.objects.all().filter(user=user),    
                                                            'skill': Skill.objects.all().filter(user=user),    
                                                            # 'interest': Interest.objects.all().filter(user=user),    
                                                            'project': Project.objects.all().filter(user=user)})    

@login_required
def newsfeed(request):
    suggestions = User.objects.exclude(id=request.user.id).order_by('?')[:3]
    return render(request, 'nucircle/newsfeed.html', {'user': request.user,
                                                     'online_user':request.user,
                                                     'suggestions':suggestions
                                                      })    

@login_required
def update_profile_image(request):
    if request.method == 'POST':
        request.user.userprofile.profile_image = request.FILES['updated_image']
        request.user.userprofile.save()    
        return redirect(reverse("nucircle:profile"))
    else:
        return redirect('nucircle:profile') 
        
@login_required
def edit_personal_info(request):
    if request.method == 'POST':

        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        # username = request.POST['username']
        name = request.POST['name']
        title = request.POST['title']
        # location = request.POST['location']
        summary = request.POST['summary']
        # discipline = request.POST['discipline']
        # graduation_year = request.POST['graduation_year']

        UserProfile.objects.get(user=User.objects.get(username=request.user.username)).update_fields(name = name, title=title, summary=summary)
        return redirect('nucircle:profile')

    else:
        return render(request, 'nucircle/profile.html', {'isOwner': True,'disciplines': list(dict(UserProfile.DISCIPLINE_CHOICES).values()) ,'error_form' : 'edit_personal_info', 'error' : '', 'user': request.user})         

@login_required
def add_education(request):
    if request.method == 'POST':

        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        institute = request.POST['institute']
        degree = request.POST['degree']
        from_year = request.POST['from_year']
        to_year = request.POST['to_year']

        isValid, message = FormValidator.add_education_validation(institute, degree, from_year, to_year)

        if not isValid:
            message['user'] = request.user
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        
        else:
            Education(user=request.user, degree=degree, from_year=from_year, to_year=to_year, institute=institute).save()
            return redirect('nucircle:profile')

    else:
        return redirect('nucircle:profile')            

@login_required
def edit_education(request, education_id = -1):

    if education_id != -1 and get_object_or_404(Education, pk=education_id).user_id != request.user.id:
        return redirect('nucircle:profile')


    if request.method == 'GET':
       education = get_object_or_404(Education, pk=education_id)
       return render(request, 'nucircle/profile.html', {    'isOwner': True,
                                                            'user': request.user, 
                                                            'error': '',
                                                            'error_form': 'edit_education',
                                                            'institute': education.institute,
                                                            'degree': education.degree,
                                                            'from_year': education.from_year,
                                                            'to_year': education.to_year,
                                                            'id': education_id})
    elif request.method == 'POST':
        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        id = request.POST['id']
        institute = request.POST['institute']
        degree = request.POST['degree']
        from_year = request.POST['from_year']
        to_year = request.POST['to_year']

        if request.POST['delete'] == 'true':
            get_object_or_404(Education, pk=id).delete()
            return redirect('nucircle:profile')
       
        isValid, message = FormValidator.edit_education_validation(institute, degree, from_year, to_year)
        if not isValid:
            message['id'] = id
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        else:
            education = get_object_or_404(Education, pk=id)
            education.update_fields(institute=institute, degree=degree, from_year=from_year, to_year=to_year)
            education.save()
            return redirect('nucircle:profile')
       
@login_required
def add_accomplishment(request):
    if request.method == 'POST':

        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        title = request.POST['title']
        institute = request.POST['institute']
        year = request.POST['year']
        
        isValid, message = FormValidator.add_accomplishment_validation(title, institute, year)

        if not isValid:
            message['user'] = request.user
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        
        else:
            Accomplishment(user=request.user, title=title, year=year, institute=institute).save()
            return redirect('nucircle:profile')

    else:
        return redirect('nucircle:profile')

@login_required
def edit_accomplishment(request, accomplishment_id = -1):

    if accomplishment_id != -1 and get_object_or_404(Accomplishment, pk=accomplishment_id).user_id != request.user.id:
        return redirect('nucircle:profile')


    if request.method == 'GET':
       accomplishment = get_object_or_404(Accomplishment, pk=accomplishment_id)
       return render(request, 'nucircle/profile.html', {    'isOwner': True,
                                                            'user': request.user, 
                                                            'error': '',
                                                            'error_form': 'edit_accomplishment',
                                                            'institute': accomplishment.institute,
                                                            'year': accomplishment.year,
                                                            'title': accomplishment.title,
                                                            'id': accomplishment_id})
    elif request.method == 'POST':
        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        id = request.POST['id']
        title = request.POST['title']
        institute = request.POST['institute']
        year = request.POST['year']

        if request.POST['delete'] == 'true':
            get_object_or_404(Accomplishment, pk=id).delete()
            return redirect('nucircle:profile')
       
        isValid, message = FormValidator.edit_accomplishment_validation(title, institute, year)
        if not isValid:
            message['id'] = id
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        else:
            accomplishment = get_object_or_404(Accomplishment, pk=id)
            accomplishment.update_fields(institute=institute, title=title, year=year)
            accomplishment.save()
            return redirect('nucircle:profile')

@login_required
def add_experience(request):
    if request.method == 'POST':

        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        title = request.POST['title']
        company = request.POST['company']
        year = request.POST['year']
        
        isValid, message = FormValidator.add_experience_validation(title, company, year)

        if not isValid:
            message['user'] = request.user
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        
        else:
            Experience(user=request.user, title=title, year=year, company=company).save()
            return redirect('nucircle:profile')

    else:
        return redirect('nucircle:profile')

@login_required
def edit_experience(request, experience_id = -1):

    if experience_id != -1 and get_object_or_404(Experience, pk=experience_id).user_id != request.user.id:
           return redirect('nucircle:profile')


    if request.method == 'GET':
       experience = get_object_or_404(Experience, pk=experience_id)
       return render(request, 'nucircle/profile.html', {    'user': request.user, 
                                                            'error': '',
                                                            'isOwner': True,
                                                            'error_form': 'edit_experience',
                                                            'company': experience.company,
                                                            'year': experience.year,
                                                            'title': experience.title,
                                                            'id': experience_id})
    elif request.method == 'POST':
        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        id = request.POST['id']
        title = request.POST['title']
        company = request.POST['company']
        year = request.POST['year']

        if request.POST['delete'] == 'true':
            get_object_or_404(Experience, pk=id).delete()
            return redirect('nucircle:profile')
       
        isValid, message = FormValidator.edit_experience_validation(title, company, year)
        if not isValid:
            message['id'] = id
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        else:
            experience = get_object_or_404(Experience, pk=id)
            experience.update_fields(company=company, title=title, year=year)
            experience.save()
            return redirect('nucircle:profile')

@login_required
def add_project(request):
    if request.method == 'POST':

        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        title = request.POST['title']
        description = request.POST['description']
        # year = request.POST['year']
        
        isValid, message = FormValidator.add_project_validation(title, description)

        if not isValid:
            message['user'] = request.user
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        
        else:
            Project(user=request.user, title=title, description=description).save()
            return redirect('nucircle:profile')

    else:
        return redirect('nucircle:profile')

@login_required
def edit_project(request, project_id = -1):

    if project_id != -1 and get_object_or_404(Project, pk=project_id).user_id != request.user.id:
        return redirect('nucircle:profile')


    if request.method == 'GET':
       project = get_object_or_404(Project, pk=project_id)
       return render(request, 'nucircle/profile.html', {    'user': request.user, 
                                                            'error': '',
                                                            'isOwner': True,
                                                            'error_form': 'edit_project',
                                                            'description': project.description,
                                                            # 'year': project.year,
                                                            'title': project.title,
                                                            'id': project_id})
    elif request.method == 'POST':
        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        id = request.POST['id']
        title = request.POST['title']
        description = request.POST['description']
        # year = request.POST['year']

        if request.POST['delete'] == 'true':
            get_object_or_404(Project, pk=id).delete()
            return redirect('nucircle:profile')
       
        isValid, message = FormValidator.edit_project_validation(title, description)
        if not isValid:
            message['id'] = id
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        else:
            project = get_object_or_404(Project, pk=id)
            project.update_fields(description=description, title=title)
            project.save()
            return redirect('nucircle:profile')

@login_required
def add_skill(request):
    if request.method == 'POST':

        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        title = request.POST['title']
        description = request.POST['description']
        
        isValid, message = FormValidator.add_skill_validation(title, description)

        if not isValid:
            message['user'] = request.user
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        
        else:
            Skill(user=request.user, title=title, description=description).save()
            return redirect('nucircle:profile')

    else:
        return redirect('nucircle:profile')

@login_required
def edit_skill(request, skill_id = -1):

    if skill_id != -1 and get_object_or_404(Skill, pk=skill_id).user_id != request.user.id:
           return redirect('nucircle:profile')

    if request.method == 'GET':

       skill = get_object_or_404(Skill, pk=skill_id)
       return render(request, 'nucircle/profile.html', {    'user': request.user, 
                                                            'error': '',
                                                            'isOwner': True,
                                                            'error_form': 'edit_skill',
                                                            'description': skill.description,
                                                            'title': skill.title,
                                                            'id': skill_id})
    elif request.method == 'POST':
        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        id = request.POST['id']
        title = request.POST['title']
        description = request.POST['description']
        
        if request.POST['delete'] == 'true':
            get_object_or_404(Skill, pk=id).delete()
            return redirect('nucircle:profile')
       
        isValid, message = FormValidator.edit_skill_validation(title, description)
        if not isValid:
            message['id'] = id
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        else:
            skill = get_object_or_404(Skill, pk=id)
            skill.update_fields(description=description, title=title)
            skill.save()
            return redirect('nucircle:profile')

@login_required
def add_interest(request):
    if request.method == 'POST':

        if request.POST['submitType'] == 'close':
            return redirect('nucircle:profile')

        selected_interests = request.POST.getlist('interest')
        isValid, message = FormValidator.add_interest_validation(selected_interests, request.user)

        if not isValid:
            message['user'] = request.user
            message['all_interests'] = AllInterests.objects.all()
            message['isOwner'] = True
            return render(request, 'nucircle/profile.html', message)
        
        else:
            for interest in selected_interests:
                Interest(user=request.user, interest=AllInterests.objects.get(name = interest)).save()
            return redirect('nucircle:profile')

    elif request.method == 'GET':    
        return render(request, 'nucircle/profile.html', {'isOwner': True,'error': '', 'error_form': 'add_interest', 'user': request.user, 'all_interests': AllInterests.objects.all()})


@login_required
def edit_interest(request):
    if request.method == 'POST':
        get_object_or_404(Interest, pk=request.POST['interest_id']).delete()
    return redirect('nucircle:profile')


@login_required
def search_results(request):
    if request.method == 'GET':
        info = DB_Helper.user_card_info(request.GET['query_string'])
        return render(request, 'nucircle/search.html', {'info': info, 'user': request.user})




@login_required
def network(request):
    following_list = DB_Helper.getFollowingList(request.user)
    follower_list = DB_Helper.get_follower_list(request.user)
    return render(request, 'nucircle/network.html', {'user': request.user, 'online_user': request.user, 'following_list': following_list, 'follower_list': follower_list})



@login_required
def add_post(request):
    if request.method == 'POST':

        if request.POST['submitType'] == 'close':
            return redirect('nucircle:newsfeed')

        if request.POST['updatePost'] == 'update':
            DB_Helper.updatePost(Post.objects.get(pk=request.POST['updatePostId']), request.POST['text'], request.FILES['filename'])
            return redirect('nucircle:newsfeed')    
            
        text = request.POST['text']
        isValid, message = FormValidator.add_post_validation(text)


        if not isValid:
            message['user'] = request.user
            message['online_user'] = request.user
            return render(request, 'nucircle/newsfeed.html', message)
        else:
            try:
                Post(user=request.user, text=text, image=request.FILES['filename']).save()
                return redirect('nucircle:newsfeed')    
            except:
                message['user'] = request.user
                message['online_user'] = request.user
                message['error'] = 'Choose an image.' 
                message['error_form'] = 'add_post'
                return render(request, 'nucircle/newsfeed.html', message)
                    
    else:
         return redirect('nucircle:newsfeed')


@login_required
def get_post(request):
    flag, posts = DB_Helper.get_post(request.user,3)
    pp = request.user.userprofile.profile_image.url
    return JsonResponse({'posts': posts,'flag':flag,'pp':pp})


@login_required
def delete_post(request):
    if(request.method == 'POST'):
        Post.objects.get(pk=request.POST['post_id']).delete()
    return redirect('nucircle:newsfeed')
    
    
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class JobView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request, format=None):
        return Response(Job.get_serialized_jobs())
    def post(self, request):
        response, status_type = Job.create_api_job(request.user, request.data)
        return Response(response, status=status_type)

class JobDetailView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request,  job_id, format=None):
        response, status_type = Job.get_api_job(job_id)
        return Response(response, status=status_type)
    def put(self, request, job_id):
        response, status_type = Job.update_api_job(request.user, request.data, job_id)
        return Response(response, status=status_type)
    def delete(self, request, job_id):
        response, status_type = Job.delete_api_job(request.user, job_id)
        return Response(response, status=status_type)

class JobApplicantListView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self,request,  job_id, format=None):
        response, status_type = Job.get_api_applicants(request.user, job_id)
        return Response(response, status=status_type)

class UserSearchView(APIView):
    def get(self, request):
        response, status_type = UserProfile.get_api_users(request)
        return Response(response, status=status_type)
         
@login_required         
def myfiles(request):
    files = File.objects.all().filter(user__id=request.user.id)
    return render(request, 'nucircle/myfiles.html',{'user':request.user,'files':files})

@login_required
def delete_file(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
    return redirect('nucircle:myfiles')

@login_required  
def upload_file(request):
    title = request.POST['title']
    file = request.FILES.get('file', False)
    
    if file:
        File.objects.create(
            title=title,
            user=request.user,
            file=file
        )
    
    return redirect('nucircle:myfiles')
           
           
@login_required
def follow_unfollow(request):
    otheruserid = request.POST['userid']
    otheruser = User.objects.get(id=otheruserid)
    list = following_list.objects.get(user=request.user)
    flag = True
    if otheruser in list.following.all():
        list.following.remove(otheruser)
        flag = False
    else:
        list.following.add(otheruser)  
        
    return JsonResponse({'flag':mark_safe(json.dumps(flag))}) 
               
           
      
@login_required
def hospital_settings(request):
    if request.user.userprofile.is_hospital_admin:     
        return render(request,'nucircle/hospital_settings.html',{})     
    return redirect('nucircle:newsfeed')      


@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, 'nucircle/change_password.html', {'msg':'Password Changed Successfully!','form':form})
        else:
            print(form.errors)
            return render(request, 'nucircle/change_password.html', {'msg':'Password not changed!','form':form})
    else:
        args = {'form': form}
        return render(request, 'nucircle/change_password.html', args)
    
    
@login_required
def change_password_hospital_settings(request):
    password = request.POST['password']
    userid = request.POST['userid']
    user = User.objects.get(id=userid)
    user.set_password(password)
    user.save()
    send_email_reset_password(request,user.email,user.username,password)
    return JsonResponse({})    


@login_required
def delete_user_hospital_settings(request):
    userid = request.POST['userid']
    user = User.objects.get(id=userid)
    user.delete()
    return JsonResponse({}) 
    
    
@login_required
def super_user_settings(request):
    if request.user.is_superuser:
        return render(request, 'nucircle/super_user_settings.html', {'requests':Category_Request.objects.all().order_by('requested_category')})
    return redirect('nucircle:newsfeed')


@login_required
def signup_hospital_admin(request):
    if request.method == 'POST':
        password_1 = request.POST['password_1']
        hcode = request.POST['hcode']
        hname = request.POST.get('hname',False) 
        email = request.POST['email']

        if User.objects.all().filter(email=email).exists():
            return JsonResponse({'message':'User with same email already exists!'})

        username = hcode + '-admin'
        
        try:
            latest_user = User.objects.all().filter(username__startswith=username).latest('id')
            count = int(latest_user.username.split('-admin')[1])
        except User.DoesNotExist:
            count = 0
        
        # count_admin = User.objects.all().filter(username__startswith = username).count()
        
        if count > 0:
            str_u = str(count+1)
            username += str_u

        user = User.objects.create_user(username=username, email=email, password=password_1)  
        user.userprofile.update_fields(location=hname,hospital_admin=True)
        send_email(request,email,username,password_1,True)
        return JsonResponse({'message':'Hospital Admin Created successfully\nUsername: '+username+'\nPassword:'+password_1})
    else:
        return render(request, 'nucircle/index.html')    
     

@login_required
def create_users_csv(request):
    file = request.FILES.get('file', False)
    
    if file.name.endswith('.xlsx'):
        return create_users_xlsx(request,file)
    
    data_set = file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    
    all_count = -1
    created_count = 0
    message = ''
    loc = request.user.userprofile.location
    
    for col in csv.reader(io_string,delimiter=','):
        all_count += 1

        if all_count > 0:
            email = col[0]
            flag = isValidEmail(email)
            if User.objects.all().filter(email=email).exists():
                message +=email+'\tDuplicate Email\n'
                
            elif flag == False or flag == None:
                message +=email+'\tIncorrect Email Format\n'     
            
            else:
                hcode = get_hospital_code(request.user.username)
                
                try:
                    latest_user = User.objects.all().filter(username__startswith=hcode+'-u').latest('id')
                    count = int(latest_user.username.split('-u')[1])
                except User.DoesNotExist:
                    count = 0
                
                username = hcode+'-u'+str(count+1)
                
                user = User.objects.create_user(username=username, email=email, password='default123')  
                user.userprofile.update_fields(location=loc)
                send_email(request,email,username,'default123',False)
                created_count += 1
                message +=email+'\t'+username+'\n'
            

    
    return JsonResponse({'all_count':all_count,'created_count':created_count,'message':message})


@login_required
def create_users_xlsx(request,file):
    # print('in xlsx')
    
    wb = openpyxl.load_workbook(file)
    worksheet = wb.active
    # print(worksheet)
    
    all_count = -1
    created_count = 0
    message = ''
    loc = request.user.userprofile.location

    for row in worksheet.iter_rows():
        # print(row[0].value)
        all_count += 1

        if all_count > 0:
            email = row[0].value
            # print(email)
            if email is not None:
                flag = isValidEmail(email)

                if User.objects.all().filter(email=email).exists():
                    message +=email+'\tDuplicate Email\n'
                    
                elif flag == False or flag == None:
                    message +=email+'\tIncorrect Email Format\n'     
                
                else:
                    hcode = get_hospital_code(request.user.username)
                    
                    try:
                        latest_user = User.objects.all().filter(username__startswith=hcode+'-u').latest('id')
                        count = int(latest_user.username.split('-u')[1])
                    except User.DoesNotExist:
                        count = 0
                    
                    username = hcode+'-u'+str(count+1)
                    
                    user = User.objects.create_user(username=username, email=email, password='default123')  
                    user.userprofile.update_fields(location=loc)
                    send_email(request,email,username,'default123',False)
                    created_count += 1
                    message +=email+'\t'+username+'\n'

    return JsonResponse({'all_count':all_count,'created_count':created_count,'message':message})


def isValidEmail(email):
    
    if len(email) > 7:
        if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
            return True
        return False
    
    
@login_required
def members_directory(request):
    return render(request,'nucircle/member_directory.html',{})   


def send_email(request,rec_email,username,password,is_super_admin):
    print('in email')
    subject = 'Congratulations! Your account on burns.pk has been created successfully.'
    message = 'The details of your account are following:\n\nUsername = ' + username + '\nPassword = '+password + '\n\nRegards,\n'+request.user.username+'\n' 
    
    if is_super_admin:
        message+='Super Admin\n'
    else:
        message+='Hospital Admin, '+request.user.userprofile.location+'\n'
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [rec_email]
    send_mail( subject, message, email_from, recipient_list )
    return True


def send_email_reset_password(request,rec_email,username,password):
    
    subject = 'Password reset successful!'
    message = 'The details of your account after reset are following:\n\nUsername = ' + username + '\nPassword = '+password + '\n\nRegards,\n'+request.user.username+'\n' 
    message+='Hospital Admin, '+request.user.userprofile.location+'\n'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [rec_email]
    send_mail( subject, message, email_from, recipient_list )
    return True


@login_required
def check_code(request):
    code = request.POST['code']
    flag = 'False'
    
    if User.objects.all().filter(username__icontains = code+'-admin').count() > 0:
        flag = User.objects.all().filter(username__icontains = code+'-admin').first().userprofile.location
    
    # print(flag)
    
    return JsonResponse({'flag':flag}) 


@login_required
def get_post_ajax(request):
    count = request.POST['count']
    flag,posts = DB_Helper.get_post(request.user,count)
    return JsonResponse({'posts': posts,'flag':flag})
    

@login_required
def like_dislike_post(request):
    postid = request.POST['postid']
    post = Post.objects.get(id=postid)
    flag = True
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        flag = False
    else:
        post.likes.add(request.user)  
        
    return JsonResponse({'flag':mark_safe(json.dumps(flag))}) 




@login_required
def get_comments_post(request):
    postid = request.POST['postid']
    comments = Post.objects.filter(id=postid).get().get_comments()
    to_send = []
    
    for c in comments:
        to_send.append({
            'commentid':c.id,
            'isAuthor':bool(request.user == c.user),    
            'username':c.user.username,
            'profile_pic':f"{settings.MEDIA_URL}{c.user.userprofile.profile_image}",
            'text':c.text
        })
        
    return JsonResponse({'comments':to_send}) 


@login_required
def submit_comments_post(request):
    postid = request.POST['postid']
    text = request.POST['text']
    
    c = Post_comment.objects.create(
        user = request.user,
        post = Post.objects.get(id=postid),
        text = text
    )
    
    to_send = {
        'commentid':c.id,
        'isAuthor':True,  
        'username':request.user.username,
        'profile_pic':f"{settings.MEDIA_URL}{request.user.userprofile.profile_image}",
        'text':text
    }
   
    return JsonResponse({'comment':to_send}) 


@login_required
def delete_comment_from_post(request):
    Post_comment.objects.get(id=request.POST['id']).delete()
    return JsonResponse({})



@login_required
def edit_comment_from_post(request):
    comment = Post_comment.objects.get(id=request.POST['commentid'])
    comment.text = request.POST['text']
    comment.save()
    return JsonResponse({})