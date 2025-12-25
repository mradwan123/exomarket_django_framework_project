from django.urls import path
from .views import checkout, process_checkout


app_name = 'transaction'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('checkout/process/', process_checkout, name='process_checkout'),


]