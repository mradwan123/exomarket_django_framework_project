from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, Cart

# Create your views here.

def home(request):
    return HttpResponse('Welcome to Home page')

############## Item Views: ################

def item_create(request):
    item  = Item.objects.create(name='Open AI secret code', description='very secret', price=10, category='tech', available=True )
    item2 = Item.objects.create(name='Database center', description='with nice chips', price=100.65, category='hardware', available=True )

    print(item)
    return HttpResponse('item added')
    
    
def item_update(request):
    item = Item.objects.filter(name='Database center').update(name='Huge Database center')
    if item:
        return HttpResponse('Found it')
    return HttpResponse('What are you looking for? entry dont exist')

def list_items(request):
    all_items = Item.objects.all()
    print(all_items)
    return HttpResponse('all items')

def item_delete(request):
    item5 = Item.objects.filter(name='Huge Database center').delete()
    
    print(item5)
    return HttpResponse(f'Item has been DELETED!')

############## Cart Views: ################

#WIP
def add_to_cart(request):
    item_obj, _ = Item.objects.get_or_create(name='new object for cart', price=20, seller_id=2)
    cart, _ = Cart.objects.get_or_create(user_id=1)
    cart.items.add(item_obj)
    print(cart.items)
    return HttpResponse('added to cart')
    
def view_cart(request):
    # view_cart = Cart.objects.all() #THIS SHOULD BE FOR ONE USER
    print(view_cart)
    return HttpResponse('view the cart in da shop')

    
def update_cart(request):
    return HttpResponse('cart updated')
