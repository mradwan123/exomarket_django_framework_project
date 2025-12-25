from django.db import models
from django.conf import settings
from users.models import User


# Create your models here.
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('shipped',   'Shipped'),
    ]
        
    buyer = models.ForeignKey(User, 
        on_delete=models.CASCADE, 
        related_name='buyer_transactions',
        null=True
        )
    seller = models.ForeignKey(User, 
            on_delete=models.CASCADE, 
            related_name='seller_transactions',
            null=True
        )
    item = models.ForeignKey(
            'shop.Item', 
            on_delete=models.CASCADE,
            related_name='transactions',
            null=True, # for testing, should be removed
        )
    transaction_date = models.DateTimeField(auto_now_add=True)  # Use DateTimeField + auto_now_add
    status = models.CharField(
            max_length=20, 
            choices=STATUS_CHOICES, 
            default='pending'
        )
        
    def __str__(self):
            return (
            f"Transaction #{self.id}: Buyer {self.buyer} → "
            f"Seller {self.seller} ({self.status})"
        )