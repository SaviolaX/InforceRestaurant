from django.db import models
from django.contrib.auth.models import AbstractUser

from restaurants.models import Restaurant


class User(AbstractUser):
    """User db table"""
    email = models.EmailField(unique=True)
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS = ('username', )

    def __str__(self) -> str:
        return self.email
