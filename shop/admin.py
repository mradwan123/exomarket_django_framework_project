from django.contrib import admin
from .models import Item, Cart, Transaction
from users.models import User

# Register your models here.

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Transaction)
