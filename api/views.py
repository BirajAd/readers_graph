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
from posts.models import Post, SharePost
from follow.models import Follow
from rest_framework.response import Response
from datetime import date, datetime
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

class FollowUser(APIView):

    def post(self,request):
        user_id = self.request.POST.get('followee_id')
    
        try:
            follow_user = User.objects.get(pk=int(user_id))
        except:
            return Response({
                "status": False,
                "details": "User doesnot exist!"    
            })
        followee_list = Follow.objects.filter(followee_id=int(user_id), follower_id = self.request.user.id).first()
        current_user = self.request.user
        the_follow = Follow()
        the_follow.follower = current_user
        the_follow.followee = follow_user
        the_follow.save()
        
        if follow_user == current_user:
            return  Response({
                "status": False,
                "details":"Bad Request: You cannot follow yourself."
            })

        if follow_user.id == followee_list.followee.id:
            return Response({
                "status": False,
                "details": "Bad Request: You have already followed this user."})
        return Response({
            "status": True,
            "details": f"You have started following {follow_user.first_name}"

        })
         
class Sharepost(APIView):
    def post(self, request, post_id):
        try:
            a_post = Post.objects.get(pk=post_id)
        except Exception as e:
            return Response({
                "status": False,
                "details": "post doesn't exist"
            })
        
        if(a_post.author == self.request.user):
            return Response({
                "status": False,
                "details": "you are author of this post."
            })

        share_post = SharePost()
        print(a_post)
        share_post.list_posts = a_post
        share_post.list_authors = self.request.user
        share_post.date = datetime.now()
        share_post.save()

        return Response({
            "status": True,
            "details": "post shared successfully"
        })

