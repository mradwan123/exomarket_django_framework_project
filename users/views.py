from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import User
# Create your views here.


# Authentication Views: 

def home(request):
    return HttpResponse('Welcome to User Home page')


def create_user(request):
    user = User.objects.create_user("username", "email", "password")
    user.first_name = "first_name"
    user.last_name = "last_name"
    user.save()

    return HttpResponse('user added')


# def loggin(request):
#     username = request.POST["username"]
#     password = request.POST["password"]
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         return HttpResponse('logged in')
#     else:
#         # Return an 'invalid login' error message
#         return HttpResponse('problem, could not logged in')

def logout_view(request):
    logout(request)
    