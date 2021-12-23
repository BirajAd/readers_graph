from django.db import models

# Create your models here.
from users.models import User
from django.utils import timezone

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followerId')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followeeId')
    timestamp = models.DateTimeField(default=timezone.now())