from django.contrib import admin
from .models import Transaction
from users.models import User

# Register your models here.

admin.site.register(Transaction)
