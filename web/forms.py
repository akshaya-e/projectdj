from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Package

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    pass 

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['title', 'destination',  'price','image','duration','description','expiry_date']
    expiry_date=forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))