from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class MultiLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email', 
        max_length=255, 
        required=False,  # Không bắt buộc
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your Multilogin email'
        })
    )
    password = forms.CharField(
        label='Password', 
        max_length=255, 
        required=False,  # Không bắt buộc
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your password'
        })
    )