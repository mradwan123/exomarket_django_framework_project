from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, Cart

# Create your views here.

def item_detail(request):
    context = {
        'user': request.user,
        'name': Item.name
    }
    
    return render(request,'item_detail_view.html', context=context )

# Item Views: 

def item_create_view(request):
    item  = Item.objects.create(name='Open AI secret code', description='very secret', price=10, category='tech', available=True )
    item2 = Item.objects.create(name='Database center', description='with nice chips', price=100.65, category='hardware', available=True )

    print(item)
    return HttpResponse('Item added')
    
    
def item_update_view(request):
    item = Item.objects.filter(name='Database center').update(name='Huge Database center')
    if item:
        return HttpResponse('Found it')
    return HttpResponse('Please check again! Das entry does not exist!')

def list_items_view(request):
    all_items = Item.objects.all()
    print(all_items)
    context = {
        'user': request.user,
        'all_items': all_items,
    }
    return render(request, 'view_all_items.html', context=context)

def item_delete_view(request):
    item5 = Item.objects.filter(name='Huge Database center').delete()
    
    print(item5)
    return HttpResponse(f'Item has been DELETED!')

# Cart Views: 

#WIP
def add_to_cart_view(request):
    item_obj, _ = Item.objects.get_or_create(name='new object for cart', price=20, seller_id=2)
    cart, _ = Cart.objects.get_or_create(user_id=1)
    cart.items.add(item_obj)
    print(cart.items)
    
    return HttpResponse('Added item to the cart in the shop')
    
# def view_user_cart_view(request):
#     cart = Cart.objects.filter(user=request.user) #THIS SHOULD BE FOR ONE USER
    
    
#     print(bool(cart))
#     if cart:
#         cart_items = cart.items.all()
#         print(cart_items)
#         context = {
#             "cart_items":cart_items,
#             "cart": cart[0]
            
#         }
#     return render(request, 'cart_view.html', context=context)

    
# def update_cart_view(request):
#     updated_item, created = Cart.objects.filter(user=request.user, item=request.item_create)
    
#     return HttpResponse('cart updated')
