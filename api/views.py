import email
from urllib import request
import json
from django.db import reset_queries
from django.http import response
from django.shortcuts import render
from follow.models import Follow
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from posts.models import Photo
from users.models import User
from posts.models import Post, SharePost, Upvote, DownVote,Comment
from follow.models import Follow
from rest_framework.response import Response
from datetime import date, datetime
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Exists


class AllPost(APIView):
    def get(self, request):
        all_posts = Post.objects.values('id', 'content', post_author=F('author__username'))
       
        for p in all_posts:
            img_path = Photo.objects.filter(post__id= p["id"]).values('id','path')
            p_upvote = Upvote.objects.filter(post__id=p["id"]).count()
            p_downvote = DownVote.objects.filter(post__id=p["id"]).count()
            p_comments = Comment.objects.filter(post__id=p["id"]).count()
            p['upvote']= p_upvote
            p['downvote']= p_downvote
            p['comments']= p_comments
            p['path']= img_path
            # print(p)

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

class PostUpvote(APIView):
    def post(self, request):
            print(json.loads(request.body)["post_id"])
            post_id = json.loads(request.body)["post_id"] 
            
            user= request.user
            if Post.objects.filter(pk= post_id).exists() == True:
                a_post = Post.objects.filter(pk= post_id).first()
                # print("sande",a_post)
                upvote = Upvote(post=a_post, user=user, date=datetime.now())
                upvote.save()
                return Response({
                    "status": True,
                    "details": "Upvoted the post."
                })
        
            else:
                return Response({
                    "status": False,
                    "details": "invalid postid"
                })
    def get(self, request):
        
            post_id = request.query_params.get("id")
            # print(post_id)
            if Upvote.objects.filter(post__id=post_id).exists() == True:
                get_upvotes = Upvote.objects.filter(post__id=post_id).values(user_info=F('user__id'), username=F('user__username'))
                return Response({
                    "status": True,
                    "details": get_upvotes
                })

            else:
                return Response({
                    "status": False,
                    "details": "invalid postId"
                })

class PostDownvote(APIView):
    def post(self, request):
        
            post_id = json.loads(request.body)["post_id"] 
            user= request.user
            if Post.objects.filter(pk= post_id).exists() == True:
                a_post = Post.objects.filter(pk= post_id).first()
                # print("sande",a_post)
                downvote = DownVote(post=a_post, user=user, date=datetime.now())
                downvote.save()
                return Response({
                    "status": True,
                    "details": "Downvoted the post."
                })
        
            else:
                return Response({
                    "status": False,
                    "details": "Invalid post id"
                })

    def get(self, request):
        
        post_id = request.query_params.get("id")
            # print(post_id)
        if DownVote.objects.filter(post__id=post_id).exists() == True: 
            get_downvotes = DownVote.objects.filter(post__id=post_id).values(user_info=F('user__id'), username=F('user__username'))
            return Response({
                "status": True,
                "details": get_downvotes
            })

        else:
            return Response({
                "status": False,
                "details": "invlaid post id"
            })

class PostComment(APIView):
    def post(self,request):
        post_id= request.POST.get("post_id")
        comment= request.POST.get("comment")
        user = request.user
        if Post.objects.filter(pk= post_id).exists() == True:
                a_post = Post.objects.filter(pk= post_id).first()
                p_comment = Comment(post=a_post, user=user, comments=comment, date=datetime.now())
                p_comment.save()
                return Response({
                    "status": True,
                    "details": "Commented on the post."
                })
        
        else:
            return Response({
                "status": False,
                "details": "Invalid post id"
            })
    
    def get(self, request):
       
        post_id = request.query_params.get("id")
            # print(post_id)
        if Comment.objects.filter(post__id=post_id).exists() == True:
            get_comments = Comment.objects.filter(post__id=post_id).values( 'comments' ,user_info=F('user__id'), username=F('user__username'))
            return Response({
                "status": True,
                "details": get_comments
            })

        else:
            return Response({
                "status": False,
                "details": "Invalid post id"
            })


class Connection(APIView):
    def get(self, request,  follow_type):
        if follow_type == "followee":
            get_followee = Follow.objects.filter(follower = request.user).values(first_name =F('followee__first_name'), userid =F("followee__id") )
            # print(get_followee)
            
            return Response({
                "status": True,
                "details": get_followee
            })

        if follow_type == 'follower':
            get_follower = Follow.objects.filter(followee = request.user).values(first_name=F('follower__first_name'), userid =F("follower__id"), email = F("follower__email"))
            # for follow in get_follower:
            #     follower = len(follow)
            #     # follow["follow"]= follower
            #     print(follow)
            
            return Response({
                "status": True,
                "details":[get_follower,len(get_follower)]
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
        # print(a_post)
        share_post.list_posts = a_post
        share_post.list_authors = self.request.user
        share_post.date = datetime.now()
        share_post.save()

        return Response({
            "status": True,
            "details": "post shared successfully"
        })

