from requests import request
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from follow.models import Follow
from users.models import User
from rest_framework.response import Response
from datetime import date, datetime
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer
from allauth import socialaccount
from allauth.socialaccount.models import SocialAccount

class GoogleLogin(SocialLoginView, TokenObtainPairView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        if(User.objects.filter(pk=self.request.user.id).first().profile_picture):
            print('exists')
        else:
            profile_pic = SocialAccount.objects.filter(user_id=self.request.user.id).first().extra_data['picture']
            user = User.objects.filter(pk=self.request.user.id).first()
            user.profile_picture = profile_pic
            user.save()

        token = MyTokenObtainPairSerializer.get_token(self.request.user)
        return Response({
            "access": str(token.access_token),
            "refresh": str(token)
        })


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

class IndividualUser(APIView):
    def get(self, request, user_id):
        
        if User.objects.filter(pk=user_id).exists():
            user = User.objects.filter(pk=user_id).values('id', 'username', 'last_active', 'first_name', 'last_name', 'bio', 'profile_picture', 'email', 'gender', 'organization', 'city', 'country')
            for u in user:
                following= Follow.objects.filter(follower=user_id).count()
                follower= Follow.objects.filter(followee=user_id).count()
                u['following']= following
                u['followers']= follower
            return Response({
                "status": True,
                "details": user
            })
        else:
            return Response({
                'status': False,
                'details': "User does not exist!!"
            })
class Users(APIView):
    
    def get(self,request):
        user =User.objects.all().exclude(pk=request.user.id).values('id', 'username', 'first_name', 'last_name', 'profile_picture', 'email')
        for u in user:
                following= Follow.objects.filter(follower=u['id']).count()
                follower= Follow.objects.filter(followee=u['id']).count()
                u["followed"]=Follow.objects.filter(follower=request.user, followee__id=u['id']).exists()
                u['following']= following
                u['followers']= follower
                
        return Response({
                "status": True,
                "details": user
            })

class LoggedInUserInfo(APIView):
    def get(self, request, *args, **kwargs):
        a_user = request.user 
        user = User.objects.filter(pk=a_user.id).values('id', 'username', 'last_active', 'first_name', 'last_name', 'bio', 'profile_picture', 'email', 'gender', 'organization', 'city', 'country', 'is_superuser')
        for u in user:
            following= Follow.objects.filter(follower=a_user).count()
            follower= Follow.objects.filter(followee=a_user).count()
            u['following']= following
            u['followers']= follower
        return Response({
            "status": True,
            "user": user
        })
        
class CreateUser(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email')
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        date_of_birth = self.request.data.get('date_of_birth')
        print(date_of_birth)
        if not password:
            return Response({
                "status": False,
                "details": "password is required"
            })
        anUser = User.objects.create_user(email, password, date_of_birth, username)
        result_user = User.objects.filter(pk=anUser.id).values('id', 'username', 'last_active', 'first_name', 'last_name', 'bio', 'profile_picture', 'email', 'gender', 'organization', 'city', 'country', 'is_superuser')
        token = MyTokenObtainPairSerializer.get_token(anUser)
        return Response({
            "access": str(token.access_token),
            "refresh": str(token),
            "user": list(result_user)
        })
