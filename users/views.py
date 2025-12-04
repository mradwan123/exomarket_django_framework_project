from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Item, User
# Create your views here.


############## Authentication Views: ################

def home(request):
    return HttpResponse('Welcome to User Home page')


def user_register_view(request):
    user1, _ = User.objects.get_or_create(username='testuser', email='test@test.com', phone_number='+49333434343', birthdate='1990-12-12')
    #user1.save()
    user2, _ = User.objects.get_or_create(username='nextuser', email='testing@testing.com', phone_number='+4933', birthdate='1900-12-12')

    return HttpResponse('user added')

def login(request):
    #check email
    return HttpResponse('Please login')