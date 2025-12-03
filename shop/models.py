from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    birthdate = models.DateField()
    
    def __str__(self):
        return f'User {self.username} added'
    
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits = 8,
        decimal_places = 2
    )
    image = models.ImageField(upload_to='item_img')
    category = models.CharField(max_length=50)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Item {self.name} costs {self.price}'
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='items')
    total_price = models.DecimalField(
        max_digits = 8,
        decimal_places = 2
    )
    
    def __str__(self):
        return f'Items of {self.user} are {self.items} with a total cost of {self.total_price}'

class Transaction(models.Model):
    buyer = models.CharField(max_length=100)
    seller = models.CharField(max_length=100)
    transaction_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return f'Buyer {self.buyer} sells to seller {self.seller}. Sale is {self.status}.'