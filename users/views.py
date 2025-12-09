from django.shortcuts import render
from django.http import HttpResponse
from .models import User
# Create your views here.


# Authentication Views: 

def home(request):
    return HttpResponse('Welcome to User Home page')


def user_register_view(request):
    user1, _ = User.objects.get_or_create(username='testuser', email='test@test.com', phone_number='+49333434343', birth_date='1990-12-12')
    #user1.save()
    user2, _ = User.objects.get_or_create(username='nextuser', email='testing@testing.com', phone_number='+4933', birth_date='1900-12-12')

    return HttpResponse('user added')

def login(request):
    user1 = request.GET.get(username='testuser')
    
    
    return HttpResponse('Please login')

# def logout(request)
    # user1 = request.GET.get(username='testuser')
    