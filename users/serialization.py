from rest_framework import serializers
from users.models import UserManager

class UserSerializer(serializers.serializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_active', 'first_name', 'last_name', 'bio', 'profile_picture', 'email', 'gender', 'organization', 'city', 'country', 'is_superuser')
        

    # def create(self, validated_data):
    #     user = UserManager.create_user(
    #         validated_data['username'],
    #         validated_data['email'],
    #         validated_data['password'],
    #         validated_data['date_of_birth']
    #     )
    
    #     return user


