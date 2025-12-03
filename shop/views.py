from django.shortcuts import render
from django.http import HttpResponse
from .models import Item

# Create your views here.

def home(request):
    return HttpResponse('Welcome to Home page')

def item_views(request):
    item = Item.objects.create(name='Open AI secret code', description='very secret', price=10, category='tech', available='yes' )
    print(item)
    print(item.query)
    
    all_items = Item.objects.all()
    print(all_items)
    