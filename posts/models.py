from datetime import datetime
from django.db import models
from datetime import datetime

from users.models import User

# Create your models here.
class Post(models.Model):
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_posts', blank=True, null=True) #original post creator
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.email+" => "+self.content


class SharePost(models.Model):
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_shared_posts", blank=True, null=True) #shared post gets deleted when user is deleted
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name="list_posts_shared", blank=True, null=True) # if original post gets deleted whole row is not deleted
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.list_posts.content

class Photo(models.Model):
    path = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='list_post_photos')

class Upvote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='list_likes')
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name='my_likes')
    date = models.DateTimeField(auto_now_add=True)

class DownVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='list_downvote')
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name='my_downvotes')
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='post_comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name='my_comments')
    comments = models.TextField(max_length=255,default='')
    date = models.DateTimeField(auto_now_add=True)