from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    EMAIL_LENGTH,
    USERNAME_LENGTH,
    FIRST_NAME_LENGTH,
    LAST_NAME_LENGTH
)


class User(AbstractUser):
    email = models.EmailField(max_length=EMAIL_LENGTH, unique=True)
    username = models.CharField(max_length=USERNAME_LENGTH, unique=True)
    first_name = models.CharField(max_length=FIRST_NAME_LENGTH)
    last_name = models.CharField(max_length=LAST_NAME_LENGTH)
    avatar = models.ImageField(
        upload_to='users/avatars/',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
