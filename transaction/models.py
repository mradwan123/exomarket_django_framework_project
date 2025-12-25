from django.db import models

# Create your models here.
class Transaction(models.Model):
    buyer = models.CharField(max_length=100, null=True)
    seller = models.CharField(max_length=100, null=True)
    transaction_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return f'Buyer {self.buyer} sells to seller {self.seller}. Sale is {self.status}.'