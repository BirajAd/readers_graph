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

class Logout(APIView):
    def get(self, request, format=None):
        token = Token.objects.get(user=request.user)
        try:
            token.delete()

            return Response({
                "status": True,
                "details": "logged out successfully"
            })
        except Exception as e:
            return Response({
                "status": False,
                "details": str(e)
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
        
class CreateUser(APIView):
    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email')
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        date_of_birth = self.request.data.get('date_of_birth')
        if not password:
            return Response({
                "status": False,
                "details": "password is required"
            })
        anUser = User.objects.create_user(email, password, date_of_birth, username)
        result_user = User.objects.filter(pk=anUser.id).values('id', 'username', 'last_active', 'first_name', 'last_name', 'bio', 'profile_picture', 'email', 'gender', 'organization', 'city', 'country', 'is_superuser')
        token, created = Token.objects.get_or_create(user=anUser)
        return Response({
            "token": token.key,
            "user": list(result_user)
        })
