from django.contrib import admin
from users.views import *
from rest_framework.authtoken import views
from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', AllPost.as_view(), name='posts'),
    path('posts/<post_id>', IndividualPost.as_view(), name='ind_post')
]