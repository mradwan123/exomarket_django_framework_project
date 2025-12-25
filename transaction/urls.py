from django.urls import path
from .views import checkout


app_name = 'transaction'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),

]