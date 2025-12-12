from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item, Cart
from .forms import ItemForm


# Home view

def home(request):
    
    context = {
        'user': request.user.username
    }
    return render(request, 'home.html', context)

# Item Views: 

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail_view.html', {'item':item}) 


def item_create_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return redirect('shop:list-seller-items', seller_id=request.user.pk)
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
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse('Success! Your Item Has Been Updated.')
        return HttpResponse('Houston, we have an issue. Invalid data was input :/ ')
    else:   
        form = ItemForm(instance=item)
        return render(request, 'update_item.html', {'form':form})


def list_items_view(request):
    all_items = Item.objects.all()
    
    context = {
        'user': request.user,
        'all_items': all_items,
    }
    return render(request, 'view_all_items.html', context=context)


def item_delete_view(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    if request.user != item.seller:
        return HttpResponse("You are not allowed to delete this item!")

    item.delete()
    return HttpResponse(f'Success!! Item {item.name} has been DELETED!')
    # return HttpResponse('Houston, we have an issue. Invalid attempt to delete :/ ')
    
    
def seller_all_items_view(request, seller_id):
   
    if request.user.pk != seller_id:
        return HttpResponse("You are not allowed to view these items. Wrong seller id. Please try again.")
    
    all_items = Item.objects.filter(seller_id=seller_id)
     
    context = {
            'all_items': all_items,
            }        
    return render(request, 'seller_all_items_view.html', context=context)
   

    

# Cart Views: 

#WIP
def add_to_cart_view(request, item_id):
    """
    Docstring for add_to_cart_view: 
    Passing item_id from url -> checking POST request - getting item details - creating cart if it doesnt exist for user
    add and saving item to cart- providing response
    
    :param request: requried for function based views in django ORM
    :param item_id: id from Item class passed in url
    """

                
    item = Item.objects.get(id=item_id) #retrieving item details from the Item calls per id=item_id
        
    cart, created = Cart.objects.get_or_create(user=request.user) #creating or accesing exists cart based on user existing
    if cart.items.filter(id=item_id).exists(): #checking to see if item already exists in the cart
        return HttpResponse("this item exists in the cart")

    cart.items.add(item)
    cart.save()
    return redirect('shop:view-cart')
            
    
def view_user_cart_view(request):
    cart_items = Cart.objects.filter(user=request.user) #THIS SHOULD BE FOR ONE USER
    # total_price = Cart.objects.filter(user=request.user)
    context = {
              'cart_items': cart_items, 
              # 'total_price': total_price,
            }
    return render(request, 'cart_view.html', context=context)

def remove_from_cart_view(request, item_id):
    pass

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
