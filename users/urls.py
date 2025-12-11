from django.urls import path
from .views import home, create_user, logout , loggin

app_name = 'users'

urlpatterns = [
    path('', home, name='home'),
    path('create/', create_user, name='create'),
    path('login/', loggin, name='login'),
    path('logout/', logout, name='logout'),

]