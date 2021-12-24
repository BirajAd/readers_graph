from django.contrib import admin
from users.views import *
from rest_framework.authtoken import views
from django.urls import path, include
from django.urls.conf import include

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'),
]