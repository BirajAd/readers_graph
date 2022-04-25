#urls.py
from unicodedata import name
from django.contrib import admin
from users.views import *
from rest_framework.authtoken import views
from django.urls import path
from .views import *


urlpatterns = [
    path('posts/', AllPost.as_view(), name='posts'),
    path('connection/<follow_type>', Connection.as_view(), name='connection'),
    path('connection/follow/',FollowUser.as_view(), name='follow'),
    path('posts/<post_id>', IndividualPost.as_view(), name='find_post'),
    path('mypost/', UserPost.as_view(), name='my_post'),
    path('sharepost/<post_id>', Sharepost.as_view(), name='share_post'),
    path('upvote_post/', PostUpvote.as_view(), name ='upvote_post'),
    path('liked_post/', LikedPosts.as_view(), name ='liked_post'),
    path('saved_post/', SavedPosts.as_view(), name ='saved_post'),
    path('downvote_post/', PostDownvote.as_view(), name ='downvote_post'),
    path('post_comment/<post_id>', PostComment.as_view(), name ='post_comment'),
    path('votecount/<post_id>', VoteCount.as_view(), name ='vote_count'),

]