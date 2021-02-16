from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, first_name=None, last_name=None):

        if username is None:
            raise TypeError("Users must have a username")
        if email is None:
            raise TypeError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_staff=False
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError("Superusers must have a password")
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):

        """
    what this does is it generates a
    JSON web token that stores current object user's instance
    and token will work for 60 days because it's expiration day
    is being set 60 days from the day the token is generated
        """

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)

        return token
