from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, User

# Create your views here.

def home(request):
    return HttpResponse('Welcome to Home page')


############## Authentication Views:

def user_create_view(request):
    user1, _ = User.objects.get_or_create(username='testuser', email='test@test.com', phone_number='+49333434343', birthdate='1990-12-12')
    #user1.save()
    user2, _ = User.objects.get_or_create(username='nextuser', email='testing@testing.com', phone_number='+4933', birthdate='1900-12-12')

    return HttpResponse('user added')

def login(request):
    return HttpResponse('Please login')

############## Authentication Views:

def item_views(request):
    item = Item.objects.create(name='Open AI secret code', description='very secret', price=10, category='tech', available=True )
    item2 = Item.objects.create(name='Database center', description='with nice chips', price=100.65, category='hardware', available=True )

    print(item)
   
    
    all_items = Item.objects.all()
    print(all_items)
    return HttpResponse('item added')
    
def item_update(request):
    item = request.GET.get('name')
    if item:
        return HttpResponse('Found it')
    return HttpResponse('What are you looking for? entry dont exist')