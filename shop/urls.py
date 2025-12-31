from django.urls import path
from .views import home, item_detail, item_create_view, item_update_view, list_items_view, item_delete_view, seller_all_items_view
from .views import add_to_cart_view, view_user_cart_view, remove_from_cart_view #, update_cart_view
from .views import search_feature, about_view
app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('items/<int:item_id>/detail/', item_detail, name='detail'),
    path('items/create', item_create_view, name='create-item'),
    path('items/<int:item_id>/update/', item_update_view, name='update'), 
    path('items/list', list_items_view, name='list'), 
    path('<int:seller_id>/items/list/', seller_all_items_view, name='list-seller-items'), 
    path('items/<int:item_id>/delete/', item_delete_view, name='delete'), 
    path('cart/<int:item_id>/add/', add_to_cart_view, name='add-to-cart'),
    path('cart/view', view_user_cart_view, name='view-cart'),
    path('cart/<int:item_id>/remove', remove_from_cart_view, name='remove-cart'),
    
    path('search/', search_feature, name='search-view'),

    path('about/', about_view, name='about')

    # path('cart/update', update_cart_view, name='update-cart'),

]