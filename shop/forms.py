from django import forms
from .models import Item, Cart


class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = [  'name',
                    'description',
                    'price',
                    'image',
                    'category', 
                    'available',
                 ]   
        
