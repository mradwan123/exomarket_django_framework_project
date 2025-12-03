from django.urls import path
from .views import home, item_views, user_auth, login, item_update

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('items/', item_views, name='items'),
    path('items/', item_update, name='items'),
    path('users/', user_auth, name='users'),
    path('login/', login, name='login'),
    
]