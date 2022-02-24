from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from users.models import User
from rest_framework.response import Response
from datetime import datetime
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

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

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class UserInfo(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        user = User.objects.filter(pk=user.id).values('id', 'username', 'last_active', 'first_name', 'last_name', 'bio', 'profile_picture', 'email', 'gender', 'organization', 'city', 'country', 'is_superuser')
        return Response({
            "status": True,
            "user": user
        })
