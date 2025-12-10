from django.urls import path
from .views import item_detail, item_create_view, item_update_view, list_items_view, item_delete_view, add_to_cart_view # view_user_cart_view #, update_cart_view

app_name = 'shop'

urlpatterns = [
    path('items/detail', item_detail, name='detail'),
    path('items/create', item_create_view, name='create-item'),
    path('items/<int:product_id>/update', item_update_view, name='update'), 
    path('items/list', list_items_view, name='list'), 
    path('items/delete', item_delete_view, name='delete'), 
    path('cart/add', add_to_cart_view, name='add-to-cart'),
    # path('cart/view', view_user_cart_view, name='view-cart'),
    # path('cart/update', update_cart_view, name='update-cart'),

]