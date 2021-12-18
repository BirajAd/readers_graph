from django.shortcuts import render
from django.db import models

# Create your views here.
class Follow(models.Model):
    follower_id = models.CharField()
