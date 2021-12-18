from django.urls import path

from . import views

urlpatterns = [
    path("", views.follow, name= "follow"),
    path("follower", views.followers, name="follower"),
    path("followee", views.followees, name="followee")
]