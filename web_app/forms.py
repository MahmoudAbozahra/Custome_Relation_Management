from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.forms.widgets import PasswordInput,TextInput

#register user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username','password1','password2']
    
    
#Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
    
    
    
#Clint form
class ClintForm(forms.ModelForm):
    class Meta:
        model = Clint  
        fields = ['first_name','last_name','phone','tall','wight','address','category'] 
   


