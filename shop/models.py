from django.db import models
from users.models import User

# Create your models here.
    
class Item(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=255, null=True)
    price = models.DecimalField(
        max_digits = 8,
        decimal_places = 2
    )
    image = models.ImageField(upload_to='item_img')
    category = models.CharField(max_length=50, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return f' Item Name: {self.name}'
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='items')
    
    @property
    def total_price(self):
        total = sum(item.price for item in self.items.all())
        return total
    
   
    def __str__(self):
        return f'Items of {self.user} are {self.items} with a total cost of {self.total_price}'

class Transaction(models.Model):
    buyer = models.CharField(max_length=100, null=True)
    seller = models.CharField(max_length=100, null=True)
    transaction_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return f'Buyer {self.buyer} sells to seller {self.seller}. Sale is {self.status}.'