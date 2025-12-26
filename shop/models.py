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
    image = models.ImageField(upload_to='item_img', null=True, blank=True)
    category = models.CharField(max_length=50, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return f' Item Name:{self.id} {self.name}'
    
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='items')
    
    @property
    def total_price(self):
        total = sum(item.price for item in self.items.all())
        return total
    
   
    def __str__(self):
        return f'Items of {self.user} are {self.items}'

