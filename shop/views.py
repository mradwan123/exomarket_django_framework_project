from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, Cart

# Create your views here.

def home(request):
    return HttpResponse('Welcome to Home page')

############## Item Views: ################

def item_create(request):
    item, _ = Item.objects.create(name='Open AI secret code', description='very secret', price=10, category='tech', available=True )
    item2, _ = Item.objects.create(name='Database center', description='with nice chips', price=100.65, category='hardware', available=True )

    print(item)
    return HttpResponse('item added')
    
    
def item_update(request):
    item = request.GET.get('name')
    Item.objects.filter(name='Database center').update(name='Huge Database center')
    if item:
        return HttpResponse('Found it')
    return HttpResponse('What are you looking for? entry dont exist')

def list_items(request):
    all_items = Item.objects.all()
    print(all_items)
    return HttpResponse('all items')

############## Cart Views: ################

#WIP
def add_to_cart(request):
    
    cart, _ = Cart.objects.get_or_create(name='new item')
    
    return HttpResponse('added to cart')
    
def view_cart(request):
    view_cart = Cart.objects.all()
    print(view_cart)
    return HttpResponse('view to cart')

    
# def update_cart(request):
#     return HttpResponse('u[dated cart')
