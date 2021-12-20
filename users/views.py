from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import User
from rest_framework.response import Response
import json

# Create your views here.
class Login(APIView):
    def post(self, request, *args, **kwargs):
        is_authenticated = authenticate(self.request.POST.get("username"), self.request.POST.get("password"))
        resp = {}
        if(is_authenticated):
            resp["status"] = True
            resp["details"]["key"] = Token.objects.get(user=request.POST.user).key
            resp["user"] = User.objects.get(user=request.POST.user)
            return Response(resp)
        else:
            return Response({"status": False, "details": "either email or password is wrong."})


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.username,
            'profile': user.profile_picture,
            'email': user.email
        })