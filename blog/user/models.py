from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, User

class CustomUser(AbstractBaseUser):
    followers = models.ManyToManyField(
        'CustomUser', related_name='followers',
        blank=True,
    )
    following = models.ManyToManyField(
        'CustomUser', related_name='following',
        blank=True,)
