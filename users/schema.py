from dataclasses import fields
from follow.models import Follow
import graphene
from graphene_django import DjangoObjectType
from posts.models import Photo, Post, SharePost
from .models import User

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"

class PhotoType(DjangoObjectType):
    class Meta:
        model = Photo
        fields = "__all__"

class FollowType(DjangoObjectType):
    class Meta:
        model = Follow
        fields = "__all__"

class SharePostType(DjangoObjectType):
    class Meta:
        model = SharePost
        fields = "__all__"

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_active', 'first_name', 'last_name', 'bio', 'profile_picture', 'email', 'gender', 'organization', 'city',\
             'country', 'is_superuser', 'list_posts', 'list_followees', 'list_followers')
    



class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    posts = graphene.List(PostType)
    # follows = graphene.List(FollowType)

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_posts(root, info, **kwargs):
        return Post.objects.all()

    # def resolve_follows(root, info, **kwargs):
    #     return Follow.objects.all()

schema = graphene.Schema(query=Query)