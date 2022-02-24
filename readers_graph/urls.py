"""readers_graph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from users.views import GoogleLogin
import users
from django.urls import path, include
from django.urls.conf import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/', include('users.urls')),
    path('api/', include('api.urls')),
    path("accounts/", include("allauth.urls")), #most important
    path('',include("users.urls")) #my app urls
]
