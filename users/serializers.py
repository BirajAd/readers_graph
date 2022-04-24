from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        # print(user.username)
        token['username'] = user.username
        token["name"] = user.first_name+' '+user.last_name
        token["email"] = user.email
        token["picture"] = user.profile_picture
        
        return token