from django.db import models
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import User
from posts.models import Post
from rest_framework.response import Response
from datetime import datetime
from django.db.models import F

# Create your views here.
# class Login(APIView):
#     def post(self, request, *args, **kwargs):
#         is_authenticated = authenticate(self.request.POST.get("username"), self.request.POST.get("password"))
#         resp = {}
#         if(is_authenticated):
#             resp["status"] = True
#             resp["details"]["key"] = Token.objects.get(user=request.POST.user).key
#             resp["user"] = User.objects.get(user=request.POST.user)
#             return Response(resp)
#         else:
#             return Response({"status": False, "details": "either email or password is wrong."})


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if(user):   
            anUser = User.objects.filter(pk=user.id)
            result_user = anUser.values('id', 'username', 'last_active', 'first_name', 'last_name', 'bio', 'profile_picture', 'email', 'gender', 'organization', 'city', 'country', 'is_superuser')
            anUser = anUser[0]
            anUser.last_active = datetime.now()
            anUser.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': list(result_user)
        })

class CreateUser(models.Model):
    def post(self, request, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('username')
        password = self.request.POST.get('password')
        password2 = self.request.POST.get('password2')
        if password != password2:
            return Response({
                "status": False,
                "details": "password should match"
            })

