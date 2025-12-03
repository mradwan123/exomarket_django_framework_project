from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, User

# Create your views here.

def home(request):
    return HttpResponse('Welcome to Home page')

def user_auth(request):
    user1, _ = User.objects.get_or_create(username='testuser', email='test@test.com', phone_number='+49333434343', birthdate='1990-12-12')
    #user1.save()
    return HttpResponse('user added')

def item_views(request):
    item = Item.objects.create(name='Open AI secret code', description='very secret', price=10, category='tech', available=True )
    print(item)
   
    
    all_items = Item.objects.all()
    print(all_items)
    return HttpResponse('item added')
    