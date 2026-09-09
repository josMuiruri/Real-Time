from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, max_length=500)
    company = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.username