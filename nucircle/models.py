from django.db import models
import re,os
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404 , redirect 
from django.core import serializers
from django.urls import reverse
from rest_framework import status

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'
def job_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'


class FormValidator:
    
    @staticmethod
    def signup_validation(username, email, password_1, password_2):
        
        if username == '':
            return False, { 'error_field': 'username',
                            'error_form' : 'signup',    
                            'error' : 'Username field is empty',
                            'username' : username,
                            'email' : email }

        
        if email == '':
            return False, { 'error_field': 'email',
                            'error_form' : 'signup',    
                            'error' : 'Email field is empty',
                            'username' : username,
                            'email' : email }
        
        if password_1 == '':
            return False, { 'error_field': 'password_1',
                            'error_form' : 'signup',    
                            'error' : 'Password 1 field is empty',
                            'username' : username,
                            'email' : email }                    

        
        if password_2 == '':
            return False, { 'error_field': 'password_2',
                            'error_form' : 'signup',    
                            'error' : 'Password 2 field is empty',
                            'username' : username,
                            'email' : email }

        if password_1 != password_2:
            return False, { 'error_field': 'password_2',
                            'error_form' : 'signup',
                            'error' : 'Passwords do not match',
                            'username' : username,
                            'email' : email }

        # if not re.match('^[A-Za-z0-9_-.]{1,}$', username):
        #     return False, { 'error_field': 'username',
        #                     'error_form' : 'signup',
        #                     'error': 'Username can only have A-Z, a-z, 0-9 or _ - .',                    
        #                     'username' : username,
        #                     'email' : email }

        if not re.match('^[A-Za-z0-9@#$%^&+=.]{8,}$', password_1):
            return False, { 'error_field': 'password_1',
                            'error_form' : 'signup',
                            'error': 'Password At least 8 characters and restricted to A-Z, a-z, 0-9 or special characters',                    
                            'username' : username,
                            'email' : email }
        try:
            user = User.objects.get(username=username)
            return False, { 'error_field': 'username',
                            'error_form' : 'signup',
                            'error': 'Username already taken', 
                            'username' : username,
                            'email' : email }
        
        except User.DoesNotExist:
                return True, {}                     
        
    @staticmethod
    def login_validation(username, password):
        
        if username == '':
            return False, { 'error_field': 'username',
                            'error_form' : 'login',    
                            'error' : 'Username field is empty',
                            'username' : username}
        
        try:
            user = User.objects.get(username=username)
        
        except User.DoesNotExist:
            return False, { 'error_field': 'username',
                            'error_form' : 'login',
                            'error': 'Username does not exist', 
                            'username' : username} 

        if password == '':
            return False, { 'error_field': 'password',
                            'error_form' : 'login',    
                            'error' : 'Password field is empty',
                            'username' : username}
      
        return True, {}                     

    @staticmethod
    def edit_personal_info_validation(username, current_username, discipline, graduation_year):
        
        if username == '':
            return False, { 'error_field': 'username',
                            'error_form' : 'edit_personal_info',    
                            'error' : 'Username field is empty',
                            'graduation_year': graduation_year,
                            'username' : username,
                            'discipline': discipline}
        
        if not re.match('^[A-Za-z0-9_]{1,}$', username):
            return False, { 'error_field': 'username',
                            'error_form' : 'edit_personal_info',
                            'graduation_year': graduation_year,
                            'discipline': discipline,
                            'error': 'Username can only have A-Z, a-z, 0-9 or _',                    
                            'username' : username}

        if graduation_year == '':
                return False, { 'error_field': 'graduation_year',
                        'error_form' : 'edit_personal_info',
                        'graduation_year': graduation_year,
                        'discipline': discipline,
                        'error': 'Graduation year field is empty',                    
                        'username' : username}
    
        
        if not re.match('^[0-9]{4}$', graduation_year) or int(graduation_year) < 1950 or int(graduation_year) > 2100:
            return False, { 'error_field': 'graduation_year',
                        'error_form' : 'edit_personal_info',
                        'graduation_year': graduation_year,
                        'discipline': discipline,
                        'error': 'Graduation year should be between 1950 and 2100',                    
                        'username' : username}


        if discipline == 'invalid':
            return False, { 'error_field': 'discipline',
                            'error_form' : 'edit_personal_info',
                            'discipline': discipline,
                            'graduation_year': graduation_year,
                            'error': 'Choose a valid discipline',                    
                            'username' : username}            


        if current_username != username:
            try:
                user = User.objects.get(username=username)
                return False, { 'error_field': 'username',
                                'error_form' : 'edit_personal_info',
                                'error': 'Username already exists',
                                'graduation_year': graduation_year,
                                'discipline': discipline, 
                                'username' : username}
            
            except User.DoesNotExist:
                    return True, {}                      
    
        return True, {}                      
    
    @staticmethod
    def add_education_validation(institute, degree, from_year, to_year):
        error = ''

        if institute == '':
            error += 'institute field is empty'    
        
        elif degree == '':
            error += 'degree field is empty'    
        
        elif from_year == '':
            error += 'from_year field is empty'    
        
        elif to_year == '':
            error += 'to_year field is empty'  
        
        elif not re.match('^[0-9]{4}$', from_year) or int(from_year) < 1950 or int(from_year) > 2100:
            error += 'Starting year should be between 1950 and 2100'
        
        elif not re.match('^[0-9]{4}$', to_year) or int(to_year) < 1950 or int(to_year) > 2100:
            error += 'Ending should be between 1950 and 2100'
        
        elif to_year < from_year:
            error += 'Ending year should be ahead of or equal to start year'      
  
        if error == '':
            return True, {}

        else:
            return False, { 'error_form': 'add_education', 
                            'error': error,
                            'institute': institute,
                            'degree': degree,
                            'from_year': from_year,
                            'to_year': to_year }    

    @staticmethod
    def edit_education_validation(institute, degree, from_year, to_year):
        isValid, message = FormValidator.add_education_validation(institute, degree, from_year, to_year)
        message['error_form'] = 'edit_education'
        return isValid, message

    @staticmethod    
    def add_accomplishment_validation(title, institute, year):
        error = ''

        if title == '':
            error += 'title field is empty'    
        
        elif institute == '':
            error += 'institute field is empty'    
        
        elif year == '':
            error += 'year field is empty'    
        
        elif not re.match('^[0-9]{4}$', year) or int(year) < 1950 or int(year) > 2100:
            error += 'year should be between 1950 and 2100'
           
        if error == '':
            return True, {}

        else:
            return False, { 'error_form': 'add_accomplishment', 
                            'error': error,
                            'institute': institute,
                            'title': title,
                            'year': year,}    

    @staticmethod
    def edit_accomplishment_validation(title, institute, year):
        isValid, message = FormValidator.add_accomplishment_validation(title, institute, year)
        message['error_form'] = 'edit_accomplishment'
        return isValid, message

    @staticmethod    
    def add_experience_validation(title, company, year):
        error = ''

        if title == '':
            error += 'title field is empty'    
        
        elif company == '':
            error += 'company field is empty'    
        
        elif year == '':
            error += 'year field is empty'    
        
        elif not re.match('^[0-9]{4}$', year) or int(year) < 1950 or int(year) > 2100:
            error += 'year should be between 1950 and 2100'
           
        if error == '':
            return True, {}

        else:
            return False, { 'error_form': 'add_experience', 
                            'error': error,
                            'company': company,
                            'title': title,
                            'year': year,}    

    @staticmethod
    def edit_experience_validation(title, company, year):
        isValid, message = FormValidator.add_experience_validation(title, company, year)
        message['error_form'] = 'edit_experience'
        return isValid, message

    @staticmethod    
    def add_project_validation(title, description):
        error = ''

        if title == '':
            error += 'title field is empty'    
        
        elif description == '':
            error += 'description field is empty'    
        
           
        if error == '':
            return True, {}

        else:
            return False, { 'error_form': 'add_project', 
                            'error': error,
                            'description': description,
                            'title': title,
                            }    

    @staticmethod
    def edit_project_validation(title, description):
        isValid, message = FormValidator.add_project_validation(title, description)
        message['error_form'] = 'edit_project'
        return isValid, message

    
    @staticmethod    
    def add_skill_validation(title, description):
        error = ''

        if title == '':
            error += 'title field is empty'    
        
        elif description == '':
            error += 'description field is empty'    
           
        if error == '':
            return True, {}

        else:
            return False, { 'error_form': 'add_skill', 
                            'error': error,
                            'description': description,
                            'title': title,}    

    @staticmethod
    def edit_skill_validation(title, description):
        isValid, message = FormValidator.add_skill_validation(title, description)
        message['error_form'] = 'edit_skill'
        return isValid, message


     
    @staticmethod    
    def add_interest_validation(selected_interests, user):
        error = ''
        if len(selected_interests) == 0:
            error += 'Select atleast one interest'

        user_current_interests = Interest.objects.all().filter(user = user).values('interest')
   
        for interest in selected_interests:
            list_value = {'interest': interest}    
            if list_value in user_current_interests:
                error += f'{interest} is already in your current interest list'
                break

        if error == '':
            return True, {}

        else:
            return False, { 'error_form': 'add_interest', 
                            'error': error}    

    @staticmethod
    def add_job_validation(title, description, company, location, tags):
        error = ''

        if company == '':
            error += 'company field is empty'    
           
        elif title == '':
            error += 'title field is empty'    
           
        elif location == '':
            error += 'location field is empty'    
           
        elif len(tags) == 0:
            error += 'Select atleast 1 job tag'    
                   
        elif description == '':
            error += 'description field is empty'    
       
        if error == '':
            return True, {}

        else:
            return False, { 'error_form': 'add_job', 
                            'error': error,
                            'description': description,
                            'title': title,
                            'company': company,
                            'location': location,}    

        
    @staticmethod    
    def add_post_validation(text):
        error = ''

        if text == '':
            error += 'Add some text'    
              
        if error == '':
            return True, {}

        else:
            return False, { 'error_form': 'add_post', 
                            'error': error,
                            'text':text}


class DB_Helper:

    @staticmethod
    def updatePost(p, text,image):
        p.text = text
        p.image = image
        p.save()

		
    @staticmethod
    def get_post(user,count):
        posts = []
        flag = True
        count = int(count)
        if count >= Post.objects.all().count():
            flag = False
            
            
        query_set = Post.objects.all().order_by('-timestamp')[count-3:count]
        for post in query_set:
            # if user in post.likes.all():
            #     fl = True
            # else:
            #     fl = False
            posts.append({
                'isMyPost': bool(user == post.user),
                'isMyLike':bool(user in post.likes.all()),
                'likes_count':post.get_likes_count(),
                'id': post.id,
                'comments_count':post.get_comment_count(),
                'username': post.user.username,
                'userid': post.user.id,
				'title': post.user.userprofile.title,
				'profile_image': f"{settings.MEDIA_URL}{post.user.userprofile.profile_image}", 
				'image': f"{settings.MEDIA_URL}{post.image}",
				'text': post.text    
			})    
        return flag,posts


    @staticmethod
    def user_card_info(query_string):
        matching_users = User.objects.all().filter(Q(username__startswith=query_string)|Q(userprofile__name__icontains=query_string)).values('id', 'userprofile', 'username','email')
        user_list = []
        for row in matching_users:
            user_info = dict()
            user_info['id'] = row['id'] 
            user_info['username'] = row['username']
            profile = UserProfile.objects.all().filter(id=row['userprofile']).values('location', 'title', 'profile_image','name')
            user_info['email'] = row['email']
            user_info['name'] = profile[0]['name']    
            user_info['location'] = profile[0]['location']
            user_info['title'] = profile[0]['title']
            user_info['profile_image'] = f"{settings.MEDIA_URL}{profile[0]['profile_image']}"
            user_list.append(user_info)
        return user_list

    @staticmethod
    def getFollowingList(user):
        friends =  following_list.objects.get(user=user).get_following_list()
        # print(friends)
        matching_users = friends.values('id', 'userprofile', 'username','email')
        user_list = []
        for row in matching_users:
            user_info = dict()
            user_info['id'] = row['id'] 
            user_info['username'] = row['username']
            profile = UserProfile.objects.all().filter(id=row['userprofile']).values('location', 'title', 'profile_image','name')
            user_info['email'] = row['email']
            user_info['name'] = profile[0]['name']    
            user_info['location'] = profile[0]['location']
            user_info['title'] = profile[0]['title']
            user_info['profile_image'] = f"{settings.MEDIA_URL}{profile[0]['profile_image']}"
            user_list.append(user_info)
        return user_list


    @staticmethod
    def get_follower_list(user):

        # pending_requests = User.objects.all().filter(id__in = FriendRequest.objects.all().filter(user_to = user.id).values('user_from'))   
        # print(pending_requests)
        # print(following_list.objects.get(user=user).get_follower_list())
        pending_requests = following_list.objects.get(user=user).get_follower_list()
        ids = []
        
        for i in pending_requests:
            ids.append(i.user.id)
            
        users = User.objects.all().filter(id__in=ids)    
        matching_users = users.values('id', 'userprofile', 'username','email')
        user_list = []
        for row in matching_users:
            user_info = dict()
            user_info['id'] = row['id'] 
            user_info['username'] = row['username']
            profile = UserProfile.objects.all().filter(id=row['userprofile']).values('location', 'title', 'profile_image','name')
            user_info['email'] = row['email']
            user_info['name'] = profile[0]['name']    
            user_info['location'] = profile[0]['location']
            user_info['title'] = profile[0]['title']
            user_info['profile_image'] = f"{settings.MEDIA_URL}{profile[0]['profile_image']}"
            user_list.append(user_info)
        return user_list


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    # graduation_year = models.IntegerField(blank=True, null=True, default=2020)
    title = models.CharField(max_length=1000, blank=True, null=True, default="Doctor")
    location = models.CharField(max_length=1000, blank=True,null=True, default="Shalamar Hospital")
    summary = models.CharField(max_length=1500, blank=True, null=True, default="Add your summary")
    profile_image = models.ImageField(upload_to=user_directory_path, default="no_image.png", blank=True, null=True) 
    is_hospital_admin = models.BooleanField(default=False)
    
    # DISCIPLINE_CHOICES = (
    #     ('Computer Science', 'Computer Science'),
    #     ('Electrical Engineering', 'Electrical Engineering'),
    #     ('Accounting and Finance', 'Accounting and Finance'),
    #     ('Civil Engineering', 'Civil Engineering'),
    #     ('Business Administration', 'Business Administration'),
    #     ('Social Sciences', 'Social Sciences'),
    #     ('Humanities', 'Humanities'),
    # )

    # discipline = models.CharField(max_length=50, choices=DISCIPLINE_CHOICES, blank=True, null=True)
    

    def __str__(self):
        return self.user.username

    def get_location_count(self):
        return UserProfile.objects.filter(location=self.location).count()
    
    def get_location_profiles(self):
        return UserProfile.objects.filter(location=self.location).order_by('-is_hospital_admin','user__username')

    def get_member_directory(self):
        return User.objects.all().order_by('username')
    
    def get_member_directory_count(self):
        return User.objects.all().count()

    def update_fields(self, **fields):
        
        if 'username' in fields:
            self.user.username = fields['username']
         
        if 'name' in fields:
            self.name = fields['name'] 
            
        if 'title' in fields:
            self.title = fields['title']
        
        if 'summary' in fields:
            self.summary = fields['summary']

        if 'location' in fields:
            self.location = fields['location']

        if 'graduation_year' in fields:
            self.graduation_year = fields['graduation_year']

        if 'discipline' in fields:
            self.discipline = fields['discipline']    
            
        if 'hospital_admin' in fields:
            self.is_hospital_admin =  fields['hospital_admin']    

        self.save()
        self.user.save()    

    @staticmethod
    def get_api_users(request):       
        username = ''
        if 'username' in request.GET:
            username = request.GET['username']
        title = ''
        if 'title' in request.GET:
            title = request.GET['title']
        location = ''
        if 'location' in request.GET:
            location = request.GET['location']
        userprofiles = []

        userprofiles = UserProfile.objects.all().filter(
            user__username__contains=username,
            title__contains=title,
            location__contains=location,
        )        
        data = []
        for profile in userprofiles:
            edu_list = []
            for edu in profile.user.education_set.all():
                edu_list.append({'institute': edu.institute, 'degree': edu.degree, 'from year': edu.from_year,'to year': edu.to_year,})        
            acom_list = []
            for acom in profile.user.accomplishment_set.all():
                acom_list.append({'institute': acom.institute,'title': acom.title,'year': acom.year,})        
            exp_list = []
            for exp in profile.user.experience_set.all():
                exp_list.append({'company': exp.company,'title': exp.title,'year': exp.year,})        
            proj_list = []
            for proj in profile.user.project_set.all():
                proj_list.append({'description': proj.description,'title': proj.title,'year': proj.year,})        
            skl_list = []
            for skl in profile.user.skill_set.all():
                skl_list.append({'description': skl.description,'title': skl.title,})        
            intr_list = []
            for intr in profile.user.interest_set.all():
                intr_list.append(intr.interest.name)
                    
            data.append({
                'username': profile.user.username,
                'email': profile.user.email,
                # 'graduation year': profile.graduation_year,
                'title': profile.title,
                'location': profile.location,
                # 'discipline': profile.discipline,
                'summary': profile.summary,
                'profile image': profile.profile_image.url,
                'education': edu_list,
                'accomplishments': acom_list,
                'experience': exp_list,
                'projects': proj_list,
                'skills': skl_list,
                'interests': intr_list,
            })
        return data, status.HTTP_200_OK
        
            
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=1000)
    degree = models.CharField(max_length=1000)
    from_year = models.IntegerField()
    to_year = models.IntegerField()

    def __str__(self):
        return self.user.username

    def update_fields(self, **fields):
      
        if 'institute' in fields:
            self.institute = fields['institute']
        
        if 'degree' in fields:
            self.degree = fields['degree']

        if 'from_year' in fields:
            self.from_year = fields['from_year']

        if 'to_year' in fields:
            self.to_year = fields['to_year']

        self.save()
        self.user.save()    

class Accomplishment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    institute = models.CharField(max_length=1000)
    year = models.IntegerField()

    def __str__(self):
        return self.user.username

    def update_fields(self, **fields):

        if 'institute' in fields:
            self.institute = fields['institute']
        
        if 'title' in fields:
            self.title = fields['title']

        if 'year' in fields:
            self.year = fields['year']

        self.save()
        self.user.save()        

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    company = models.CharField(max_length=1000)
    year = models.IntegerField()

    def __str__(self):
        return self.user.username

    def update_fields(self, **fields):
        
        if 'title' in fields:
            self.title = fields['title']

        if 'company' in fields:
            self.company = fields['company']

        if 'year' in fields:
            self.year = fields['year']

        self.save()
        self.user.save()     


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    # year = models.IntegerField()
    description = models.CharField(max_length=1500)

    def __str__(self):
        return self.user.username

    def update_fields(self, **fields):
        
        if 'title' in fields:
            self.title = fields['title']

        if 'description' in fields:
            self.description = fields['description']


        self.save()
        self.user.save()     

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1500)

    def __str__(self):
        return self.user.username

    def update_fields(self, **fields):
        
        if 'title' in fields:
            self.title = fields['title']

        if 'description' in fields:
            self.description = fields['description']

        self.save()
        self.user.save()            


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    text = models.CharField(max_length=3000,default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=user_directory_path, default="no_image.png", blank=True, null=True)  
    likes = models.ManyToManyField(
            User, related_name='likes_post')
    
    def get_likes_count(self):
        return self.likes.all().count()

    def get_comment_count(self):
        return Post_comment.objects.all().filter(post=self).order_by('user__username').count()
    
    def get_comments(self):
        return Post_comment.objects.all().filter(post=self).order_by('user__username')

    def __str__(self):
        return self.text
 
 
class Post_comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000,default="comment...")   
    
    def __str__(self):
        return self.user.username + ' commented on post '+ str(self.post.id)  

class File(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)


    def __str__(self):
        return (self.title + " uploaded by " + self.user.username) 

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
        
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension    
        
        
class following_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        User, related_name='following') 
    
    def __str__(self):
        return self.user.username  
    
    def get_following_list(self):
        return self.following.all()          
    
    def get_follower_list(self):
        id = self.user.pk
        return following_list.objects.all().filter(following__in=[id]) 
        