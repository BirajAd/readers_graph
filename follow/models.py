from datetime import datetime
from django.db import models

# Create your models here.
from users.models import User
from django.utils import timezone

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_followees')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_followers')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.email+f"{self.follower.id} follows {self.followee.id}"+self.followee.email
