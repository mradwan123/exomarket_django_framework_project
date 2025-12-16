from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
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
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:home')
    else:
        form = UserForm()
    
    return render(request, 'create.html', {'form':form})
   
@login_required
def profile(request):
    return render(request, 'profile.html')

def logout_custom(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')
    return render(request, 'logout_confirm.html')


# def loggin(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
            
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 # Redirect to a success page.
#                 return redirect('home')
#             else:
#                 # Return an 'invalid login' error message
#                 return HttpResponse('problem, could not logged in')


    