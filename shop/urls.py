from django.urls import path
from .views import home, item_create, item_update, add_to_cart, view_cart

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('items/create', item_create, name='create'),
    path('items/update', item_update, name='update'), 
    path('cart/add', add_to_cart, name='add-to-cart'),
    path('cart/view', view_cart, name='view-cart'),


    
]