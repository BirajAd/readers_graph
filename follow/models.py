from datetime import datetime
from django.db import models

# Create your models here.
from users.models import User
from django.utils import timezone

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_followers')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_followees')
    timestamp = models.DateTimeField(default=timezone.now())
