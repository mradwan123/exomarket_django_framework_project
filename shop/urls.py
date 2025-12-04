from django.urls import path
from .views import home, item_create, item_update

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('items/create', item_create, name='create'),
    path('items/update', item_update, name='update'), #same parent folder??

    
]