from dataclasses import fields
import graphene
from graphene_django import DjangoObjectType
from posts.models import Post
from .models import User

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_active', 'first_name', 'last_name', 'bio', 'profile_picture', 'email', 'gender', 'organization', 'city', 'country', 'is_superuser')
    posts = graphene.List(PostType)

    def resolve_posts(self, info):
        return self.posts.all()



class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    posts = graphene.List(PostType)

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_posts(root, info, **kwargs):
        return Post.objects.all()

schema = graphene.Schema(query=Query)