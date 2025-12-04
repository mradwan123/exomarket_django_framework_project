from django.urls import path
from .views import home, user_register_view, login

app_name = 'users'

urlpatterns = [
    path('', home, name='home'),
    path('register/', user_register_view, name='register'),
    path('login/', login, name='login'),
]