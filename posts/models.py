from django.db import models

from users.models import User

# Create your models here.
class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    content = models.TextField(blank=True)
    author = models.ManyToManyField(User)

