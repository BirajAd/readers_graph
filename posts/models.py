from datetime import datetime
from django.db import models
from datetime import datetime

from users.models import User

# Create your models here.
class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_posts', blank=True, null=True) #original post creator
    post_date = models.DateTimeField()

    def __str__(self):
        return self.author.email+" => "+self.content


class SharePost(models.Model):
    id = models.IntegerField(primary_key=True)
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_shared_posts", blank=True, null=True) #shared post gets deleted when user is deleted
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name="list_posts_shared", blank=True, null=True) # if original post gets deleted whole row is not deleted
    date = models.DateTimeField()

    def __str__(self):
        return self.list_posts.content

class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='list_post_photos')
