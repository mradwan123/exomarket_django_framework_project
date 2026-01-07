from django import forms
from django.contrib.admin.widgets import AdminDateWidget 

from .models import User


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'bio', 'birth_date']
        widgets = {  
            "birth_date": AdminDateWidget(),  # Replace default widget with AdminDateWidget  
        }  
        
    def save(self):
        """Save user with hashed password"""
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            bio = self.cleaned_data['bio'],
            phone_number = self.cleaned_data['phone_number'],
            birth_date = self.cleaned_data['birth_date'],
        )
        
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
 