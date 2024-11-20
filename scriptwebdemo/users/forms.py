from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập mật khẩu',
            'style': 'width: 500px;'
        }),
    )
    password2 = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xác nhận mật khẩu',
            'style': 'width: 500px;'
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'style': 'width: 500px;'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'style': 'width: 500px;'
            }),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'style': 'width: 500px;'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'style': 'width: 500px;'})
    )

    class Meta:
        fields = ['username', 'password']


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
