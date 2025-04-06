from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(default="", max_length=100)
    last_name = models.CharField(default="", max_length=100)
    phone_number = models.CharField(default="", max_length=15, unique=True)

    def __str__(self):
        return self.username
