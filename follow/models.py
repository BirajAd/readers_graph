from datetime import datetime
from django.db import models

# Create your models here.
from users.models import User
from django.utils import timezone

class Follow(models.Model):
    follower_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followerId')
    followee_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followeeId')
    timestamp = models.DateTimeField(default=datetime.now())