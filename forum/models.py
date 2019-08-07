from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from nucircle.models import File
from django.db import models
from django.db.models import Count

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        'Forum_Post', related_name='comments', on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        User, related_name='likes')

    def __str__(self):
        return (self.user.username +" has commented on "+ self.post.title)
    

class Forum_Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    files = models.ManyToManyField(
        File, related_name='forum_files')
     
       
    def __str__(self):
        return self.title
    
    @property
    def get_comments(self):
        return Comment.objects.filter(post=self).annotate(likes_o=Count('likes')).order_by('-likes_o')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    
class Category_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_category = models.CharField(max_length=20)
    
    def __str__(self):
        return (self.user.username +" requested #"+ self.requested_category)