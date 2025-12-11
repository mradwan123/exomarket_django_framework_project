from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item, Cart
from .forms import ItemForm

# Create your views here.

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail_view.html', {'item':item}) 

# Item Views: 

def item_create_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return HttpResponse('Item was created and added to database.')
        return HttpResponse('Invalid input')
    else:
        form = ItemForm
        return render(request, 'create_item.html', {'form':form}) 

    
    
def item_update_view(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    print(item.id)
    if request.user != item.seller:
        return HttpResponse("You are not allowed to update this item!")
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse('Success! Your Item Has Been Updated.')
        return HttpResponse('Houston, we have an issue. Invalid data was input :/ ')
    else:   
        form = ItemForm(instance=item)
        return render(request, 'update_item.html', {'form':form})

def list_items_view(request):
    all_items = Item.objects.all()
    print(all_items)
    context = {
        'user': request.user,
        'all_items': all_items,
    }
    return render(request, 'view_all_items.html', context=context)

def item_delete_view(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    if request.user != item.seller:
        return HttpResponse("You are not allowed to delete this item!")

    item_name = item.name
    item.delete()
    return HttpResponse(f'Success!! Item {item_name} has been DELETED!')
    # return HttpResponse('Houston, we have an issue. Invalid attempt to delete :/ ')

    

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
