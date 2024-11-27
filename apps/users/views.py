from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomLoginForm, User
from django.contrib import messages
from ..multilogin.models import MultiloginAccount
from ..scripts.views import get_script
from ..actions.actions import WebAutomation


def home(request):
    multilogin_accounts = []
    scripts = []
    web_automation = WebAutomation(None)
    if request.user.is_authenticated:
        scripts = get_script(request)
        multilogin_accounts = MultiloginAccount.objects.filter(
            user=request.user).values()
        actions = web_automation.get_action_list()
    return render(request, 'home.html', {'scripts': scripts, 'multilogin_accounts': multilogin_accounts, 'actions': actions})


def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
        else:
            print(form.errors)
            return render(request, 'login.html', {'form': form})
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'email already exists')
            else:
                form.save()
                password = form.cleaned_data.get('password1')
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('home')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('home')


@login_required
def user(request):
    multilogin_accounts = []
    # multilogin_accounts = get_multilogin_accounts(user=request.user).value()
    multilogin_accounts = MultiloginAccount.objects.filter(
        user=request.user).values()
    email = multilogin_accounts[0]['email'] if multilogin_accounts else ''
    return render(request, 'user.html', {'multilogin_accounts': multilogin_accounts, "email": email})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # update session to prevent user from being logged out
            update_session_auth_hash(request, user)
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {'form': form})
