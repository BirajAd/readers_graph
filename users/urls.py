from django.contrib import admin
from users.views import *
from rest_framework.authtoken import views
from django.urls import path, include
from django.urls.conf import include
from . import views

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', Logout.as_view()),
    path('userinfo/', UserInfo.as_view(), name='userinfo'),
    path('register/', CreateUser.as_view(), name='register')
]