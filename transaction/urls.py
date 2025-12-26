from django.urls import path
from .views import checkout, process_checkout, transaction_success


app_name = 'transaction'

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('checkout/process/', process_checkout, name='process-checkout'),
    path('success', transaction_success, name='transaction-success'),


]