from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

phone_regex = RegexValidator(
    regex=r'^\+?[0-9]{7,15}$',             
    message=(
        "Enter a valid phone number. It can start with '+', "
        "followed by 7-15 digits."
    ),
)

class User(AbstractUser):
    '''Custom User model extending/adding to AbstractUser.'''
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,                # allow empty form submissions
        validators=[phone_regex],
    )

    def __str__(self):
        return f'{self.username}'
    
    