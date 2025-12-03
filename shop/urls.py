from django.urls import path
from .views import home, item_views, user_create_view, login, item_update

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('items/', item_views, name='items'),
    path('items/', item_update, name='items'),
    path('users/', user_create_view, name='users'),
    path('users/login/', login, name='login'),
    
]