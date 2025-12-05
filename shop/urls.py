from django.urls import path
from .views import home, item_create, item_update, list_items, item_delete, add_to_cart, view_cart, update_cart

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('items/create', item_create, name='create'),
    path('items/update', item_update, name='update'), 
    path('items/list', list_items, name='list'), 
    path('items/delete', item_delete, name='delete'), 
    path('cart/add', add_to_cart, name='add-to-cart'),
    path('cart/view', view_cart, name='view-cart'),
    path('cart/update', update_cart, name='view-cart'),

]