from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction as db_transaction
from django.utils import timezone
from shop.models import Cart, Item
from users.models import User
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
        'user': request.user
    }
    return render(request, 'checkout.html', context)


def process_checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('shop:cart')
    
    try:
        with db_transaction.atomic():
            # Create a transaction for each item in the cart
            transactions_created = []
            
            for item in cart.items.all():
                # Check if item is still available
                if not item.available:
                    messages.error(request, f"{item.name} is no longer available!")
                    continue
                
                # Prevent users from buying their own items
                if item.seller == request.user:
                    messages.warning(request, f"You cannot buy your own item: {item.name}")
                    continue
                
                # Create transaction
                transaction_obj = Transaction.objects.create(
                    buyer=request.user,
                    seller=item.seller,
                    item=item,
                    transaction_date=timezone.now(),
                    status='pending'  # or 'completed' depending on your workflow
                )
                
                # Mark item as unavailable (sold)
                item.available = False
                item.save()
                
                transactions_created.append(transaction_obj)
            
            # Clear the cart
            cart.items.clear()
            
            if transactions_created:
                messages.success(
                    request, 
                    f"Successfully purchased {len(transactions_created)} item(s)!"
                )
                return redirect('shop:transaction_success')
            else:
                messages.error(request, "No valid items were purchased.")
                return redirect('shop:cart')
            
    except Exception as e:
        messages.error(request, f"An error occurred during checkout: {str(e)}")
        return redirect('shop:cart')
