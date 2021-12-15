from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(null=True)
    last_active = models.DateTimeField(null=True)
    profile_picture = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=200, unique=True)
    gender = models.CharField(max_length=10, null=True)
    is_staff = models.BooleanField()
    is_admin = models.BooleanField()
    organization = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=150, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        return self.first_name+" "+self.last_name

    @property
    def is_staff(self):
        return self.is_staff

    @property
    def is_admin(self):
        return self.is_admin