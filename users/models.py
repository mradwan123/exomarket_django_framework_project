from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
   
class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    """
    # username = models.CharField(max_length=50, null=True)
    # email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.username}'
    
    