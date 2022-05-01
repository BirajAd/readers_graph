
from follow.models import Follow
from rest_framework.views import APIView
from posts.models import Photo
from users.models import User
from posts.models import Post, SharePost, Upvote, DownVote,Comment, SavedPost
from follow.models import Follow
from rest_framework.response import Response
from datetime import date, datetime
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Exists
from django.core.files.storage import default_storage
import boto3 as aws
from django.conf import settings
from datetime import datetime

class AllPost(APIView):
    def get(self, request):
        all_posts = Post.objects.values('id', 'content', post_author=F('author__username'), firstname=F('author__first_name'), lastname = F('author__last_name'), \
                    profile_p = F('author__profile_picture'), userId=F('author__id'))
       
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
         photos = request.FILES.getlist('filename')
         print(photos)
         an_user = self.request.user
        #  the_post = Post()
        #  the_post.content = content
        #  the_post.save()
         the_post = Post.objects.create(content=content, author=an_user)

         for file in photos:
             print(the_post)
             filename = str(datetime.now())+ "_" + str(file)
             ast = default_storage.save(filename,file)
             response = settings.CLOUD_FRONT + str(filename)
             
             photo = Photo.objects.create(path=response, post=the_post)
             print(photo)

         return Response({
             "status": True,
             "details": "posted successfully"
         })

class IndividualPost(APIView):
    def get(self, request, post_id):
        a_post = Post.objects.filter(pk=post_id).values('id', 'content', post_author=F('author__username'), firstname=F('author__first_name'), lastname = F('author__last_name'), \
                    profile_p = F('author__profile_picture'), userId=F('author__id'))
        for p in a_post:
            img_path = Photo.objects.filter(post__id= p["id"]).values('id','path')
            p_upvote = Upvote.objects.filter(post__id=p["id"]).count()
            p_downvote = DownVote.objects.filter(post__id=p["id"]).count()
            p_comments = Comment.objects.filter(post__id=p["id"]).count()
            p['upvote']= p_upvote
            p['downvote']= p_downvote
            p['comments']= p_comments
            p['path']= img_path

        return Response({
            "status": True,
            "details": a_post
        })
        
class UserPost(APIView):
    def get(self, request):
        user= request.user
        user_post = Post.objects.filter(author=user).values('id', 'content',post_author=F('author__username'), firstname=F('author__first_name'), lastname = F('author__last_name'), \
                    profile_p = F('author__profile_picture'))
        for p in user_post:
            img_path = Photo.objects.filter(post__id= p["id"]).values('id','path')
            p_upvote = Upvote.objects.filter(post__id=p["id"]).count()
            p_downvote = DownVote.objects.filter(post__id=p["id"]).count()
            p_comments = Comment.objects.filter(post__id=p["id"]).count()
            p['upvote']= p_upvote
            p['downvote']= p_downvote
            p['comments']= p_comments
            p['path']= img_path

        return Response({
            "status": True,
            "details":user_post
        })

class PostUpvote(APIView):
    def post(self, request):
            print(request.data["post_id"])
            post_id = request.data["post_id" ]
            
            user= request.user
            if Post.objects.filter(pk= post_id).exists():
                a_post = Post.objects.filter(pk= post_id).first()
                print("sande",a_post)
                if Upvote.objects.filter(post= a_post,user = user).exists():
                    Upvote.objects.filter(post= a_post,user = user).delete()
                    count = Upvote.objects.filter(post= a_post).count()
                    return Response({
                        "status": True,
                        "details": count
                    })

                else:
                    upvote = Upvote(post=a_post, user=user, date=datetime.now())
                    upvote.save()
                    count = Upvote.objects.filter(post= a_post).count()
                    return Response({
                        "status": True,
                        "details": count
                    })
            else:
                return Response({
                    "status": False,
                    "details": "post has been deleted by the author"
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

class LikedPosts(APIView):
    def get(self,request):
        user= request.user
        liked_posts = Upvote.objects.filter(user__id=user.id).values( 'post','user', content=F('post__content'),  post_author=F('post__author__username'), firstname=F('post__author__first_name'), lastname = F('post__author__last_name'), \
                        profile_p = F('post__author__profile_picture'))

        for p in liked_posts:
            img_path = Photo.objects.filter(post__id= p["post"]).values_list('path',flat=True)
            p_upvote = Upvote.objects.filter(post__id=p["post"]).count()
            p_downvote = DownVote.objects.filter(post__id=p["post"]).count()
            p_comments = Comment.objects.filter(post__id=p["post"]).count()
            p['upvote']= p_upvote
            p['downvote']= p_downvote
            p['comments']= p_comments
            p['path']= img_path
        return Response({
            "status": True,
            "details": liked_posts
        })



class VoteCount(APIView):
    def get(self, request, post_id):
        upvote_count = Upvote.objects.filter(post__id = post_id).count()
        return Response({
            "status": True,
            "details":upvote_count
        })

class SavedPosts(APIView):
    def post(self, request):
            print(request.data["post_id"])
            post_id = request.data["post_id" ]
            user= request.user
            if Post.objects.filter(pk= post_id).exists():
                a_post = Post.objects.filter(pk= post_id).first()
                print("sande",a_post)
                if SavedPost.objects.filter(post= a_post,user = user).exists():
                    SavedPost.objects.filter(post= a_post,user = user).delete()
                    return Response({
                        "status": True,
                        "details":"Unsaved the post"
                    })

                else:
                    saved_post = SavedPost(post=a_post, user=user, date=datetime.now())
                    saved_post.save()
                    print("hello",saved_post)
                    return Response({
                        "status": True,
                        "details": "Saved the post."
                    })

        
            else:
                return Response({
                    "status": False,
                    "details": "invalid postid"
                })
                
    def get(self, request):
            user= request.user
            get_saved = SavedPost.objects.filter(user__id=user.id).values( 'post','user', content=F('post__content'),  post_author=F('post__author__username'), firstname=F('post__author__first_name'), lastname = F('post__author__last_name'), \
                        profile_p = F('post__author__profile_picture'))

            for p in get_saved:
                img= Photo.objects.filter(post__id=p['post']).values_list('path', flat=True)
                p_upvote = Upvote.objects.filter(post__id=p["post"]).count()
                p_downvote = DownVote.objects.filter(post__id=p["post"]).count()
                p_comments = Comment.objects.filter(post__id=p["post"]).count()
                p["photos"]= img
                p['upvote']= p_upvote
                p['downvote']= p_downvote
                p['comments']= p_comments

                
            return Response({
                "status": True,
                "details": get_saved
            })

           
class PostDownvote(APIView):
    def post(self, request):
        
            post_id = request.data["post_id" ]
            user= request.user
            if Post.objects.filter(pk= post_id).exists() == True:
                a_post = Post.objects.filter(pk= post_id).first()
                if DownVote.objects.filter(post= a_post,user = user).exists():
                    DownVote.objects.filter(post= a_post,user = user).delete()
                    return Response({
                        "status": True,
                        "details":"Undid the downvote."
                    })

                else:
                    downvote = DownVote(post=a_post, user=user, date=datetime.now())
                    downvote.save()
                    return Response({
                        "status": True,
                        "details": "Downvoted the post."
                    })
                # print("sande",a_post)
               
        
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
    def post(self,request,post_id):
        # post_id = request.data["post_id" ]
        comment= request.data["comment"]
        user = request.user
        if Post.objects.filter(pk= post_id).exists() == True:
                a_post = Post.objects.filter(pk= post_id).first()
                p_comment = Comment(post=a_post, user=user, comments=comment, date=datetime.now())
                p_comment.save()
                return Response({
                    "status": True,
                    "details": list(Comment.objects.filter(pk=p_comment.id).values('comments' ,user_info=F('user__id'), username=F('user__username')\
                , profile = F('user__profile_picture')))
                })
        
        else:
            return Response({
                "status": False,
                "details": "Invalid post id"
            })
    
    def get(self, request,post_id):
       
        # post_id = request.query_params.get("id")
        print(post_id)
        if Comment.objects.filter(post__id=post_id).exists() == True:
            get_comments = Comment.objects.filter(post__id=post_id).order_by('-date').values('id', 'comments' ,user_info=F('user__id'), username=F('user__username')\
                , profile = F('user__profile_picture'))
            return Response({
                "status": True,
                "details": get_comments
            })
            
        else:
            return Response({
                "status": False,
                "details": []
            })


class Connection(APIView):
    def get(self, request,  follow_type):
        user_id = request.query_params.get('user_id')
        if follow_type == "followee":
            get_followee = Follow.objects.filter(follower__id = user_id).values(first_name =F('followee__first_name'),last_name=F('followee__last_name'), userid =F("followee__id"), \
             username=F("followee__username"),profile_p = F('followee__profile_picture'))
            # print(get_followee)
            
            return Response({
                "status": True,
                "details": get_followee
            })

        if follow_type == 'follower':
            get_follower = Follow.objects.filter(followee = request.user).values(first_name=F('follower__first_name'),last_name=F('follower__last_name'), userid =F("follower__id"), \
                 email = F("follower__email"),username=F("follower__username"),profile_p = F('follower__profile_picture'))
            # for follow in get_follower:
            #     follower = len(follow)
            #     # follow["follow"]= follower
            #     print(follow)
            
            return Response({
                "status": True,
                "details":get_follower
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

