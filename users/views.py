from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import UserForm
# Create your views here.


# Authentication Views: 

def home(request):
    context = {
        'user': request.user.username
    }
    return render(request, 'home.html', context=context)


def create_user(request):
    user = User.objects.create_user("username", "email", "password")
    user.first_name = "first_name"
    user.last_name = "last_name"
    user.save()

    return HttpResponse('user added')


def loggin(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('home')
            else:
                # Return an 'invalid login' error message
                return HttpResponse('problem, could not logged in')

def logout_view(request):
    logout(request)
    