from django.urls import path
from .views import home, create_user, profile , logout_custom, login_custom, update_profile
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('home', home, name='home'),
    path('create/', create_user, name='create'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
    path('profile/', profile, name='profile'),
    path('logout/', logout_custom, name='logout'),
    path('login/', login_custom, name='login'),
    path('update/', update_profile, name='update-profile'),

]