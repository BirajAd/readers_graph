from django.contrib import admin
from users.views import *
from rest_framework.authtoken import views
from django.urls import path
from .views import *


urlpatterns = [
    path('posts/', AllPost.as_view(), name='posts'),
    path('connection/<follow_type>', Connection.as_view(), name='connection'),
    path('posts/<post_id>', IndividualPost.as_view(), name='find_post'),
    path('sharepost/<post_id>', Sharepost.as_view(), name='share_post')
]