# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
    def create_user(self, email, password, date_of_birth, username):
        if not email:
            return ValueError("you must have an email address.")
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, username, password):
        if not email:
            return ValueError("you must have an email address.")
        user = self.create_user(
            email = email,
            date_of_birth=date_of_birth,
            password=password,
            username=username,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    bio = models.TextField()
    username = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(null=True)
    last_active = models.DateTimeField(null=True)
    profile_picture = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=200, unique=True)
    gender = models.CharField(max_length=10, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    organization = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=150, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'username']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name+" "+self.last_name

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_admin(self):
        return self.is_admin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
