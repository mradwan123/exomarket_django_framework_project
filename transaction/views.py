from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shop.models import Cart, Item
from .models import Transaction
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def checkout(request):
    """
    Display checkout page with cart summary
    """
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('shop:cart')
    
    context = {
        'cart': cart,
        'total_price': cart.total_price,
    }
    return render(request, 'checkout.html', context)

