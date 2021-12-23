from django.db import reset_queries
from django.http import response
from django.shortcuts import render
import follow
from follow.models import Follow
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import User
from posts.models import Post
from follow.models import Follow
from rest_framework.response import Response
from datetime import datetime
from django.db.models import F


class AllPost(APIView):
    def get(self, request):
        all_posts = Post.objects.values('id', 'content', post_author=F('author__username'))
        return Response({
            "status": True,
            "details": all_posts 
        })

    def post(self, request):
         content = self.request.POST.get('content')
         an_user = self.request.user
         the_post = Post()
         the_post.content = content
         the_post.save()
         return Response({
             "status": True,
             "details": "posted successfully"
         })

class IndividualPost(APIView):
    def get(self, request, post_id):
        a_post = Post.objects.filter(pk=post_id).values('id', 'content', post_author=F('author__username'))
        return Response({
            "status": True,
            "details": a_post
        })
class Connection(APIView):
    def get(self, request,  follow_type):
        if follow_type == "followee":
            
            get_followee = Follow.objects.filter(follower = request.user).values(first_name =F('followee__first_name'))
            return Response({
                "status": True,
                "details": get_followee
            })

        if follow_type == 'follower':
            get_follower = Follow.objects.filter(followee = request.user).values(first_name=F('follower__first_name'))
            return Response({
                "status": True,
                "details": get_follower
            })