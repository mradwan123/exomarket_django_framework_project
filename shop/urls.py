from django.urls import path
from .views import home, item_views

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('items', item_views, name='items'),
    
]