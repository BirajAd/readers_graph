from datetime import datetime
from django.db import models
from datetime import datetime

from users.models import User

# Create your models here.
class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) #original post creator
    post_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.author.email+" => "+self.content


class SharePost(models.Model):
    id = models.IntegerField(primary_key=True)
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, name="list_authors") #shared post gets deleted when user is deleted
    post = models.ForeignKey(Post, on_delete=models.PROTECT, name="list_posts") # if original post gets deleted whole row is not deleted
    date = models.DateTimeField(default=datetime.now())