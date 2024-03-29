from django.contrib import admin
from users.views import *
from rest_framework.authtoken import views
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.urls.conf import include
from . import views
from users.schema import schema

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', Logout.as_view()),
    path('loggedinuserinfo/', LoggedInUserInfo.as_view(), name='loggedinuserinfo'),
    path('users/', Users.as_view(), name='users'),
    path('users/<user_id>', IndividualUser.as_view(), name='users'),
    path('register/', CreateUser.as_view(), name='register'),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema))
]