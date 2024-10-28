from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, MultiLoginForm
from .models import MultiloginAccount
from .multilogindriver import signin, profile_search
from django.contrib import messages
import datetime
import sys
from .utils import get_multilogin_accounts  
from .multilogindriver import setDriver as multiloginSetDriver, stop_profile as multiloginDestroyDriver
from .script.game2048 import game_run
from .script.foxnews import fox_news_run
from .script.surfing_script import surfing_script_run
from .script.surfing_jomashop import surfing_jomashop_run
from .script.surfing_ebay import    surfing_ebay_run
from .script.surfing_macys import surfing_macys_run

def home(request):
    user=request.user
    scripts = [
        {'name': 'Tìm kiếm theo keywords', 'func': 'surfing_script_run'},
        {'name': 'Lướt web macys', 'func': 'surfing_macys_run'},
        {'name': 'Lướt web jomashop', 'func': 'surfing_jomashop_run'},
        {'name': 'Lướt web ebay', 'func': 'surfing_ebay_run'},
        {'name': 'Chơi game 2048', 'func': 'game_run'},
        {'name': 'Đọc báo trên Fox', 'func': 'fox_news_run'}
    ]
    multilogin_accounts = []
    if user.is_authenticated:
        multilogin_accounts = MultiloginAccount.objects.filter(user=request.user).values()
    return render(request, 'home.html', {'scripts': scripts, 'multilogin_accounts': multilogin_accounts})   

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
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
    multilogin_accounts = MultiloginAccount.objects.filter(user=request.user).values()
    email = multilogin_accounts[0]['multilogin_email'] if multilogin_accounts else ''
    return render(request, 'user.html',{'multilogin_accounts':multilogin_accounts, "email": email})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # update session to prevent user from being logged out
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {'form': form})

@login_required
def multilogin(request):
    if request.method == 'POST':
        form = MultiLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Đăng nhập vào Multilogin và lấy token
            token = signin(email, password)
            if token:
                data = profile_search()
                for profile in data:
                    multilogin_account, created = MultiloginAccount.objects.get_or_create(
                        user=request.user,
                        multilogin_profile_id=profile.get('id', ''),
                        defaults={
                            'multilogin_email': email,
                            'multilogin_password': password,
                            'multilogin_token': token,
                            'multilogin_folder_id': profile.get('folder_id', ''),
                            'multilogin_profile_name': profile.get('name', '')
                        }
                    )
                    if not created:
                        # Cập nhật thông tin nếu tài khoản đã tồn tại
                        multilogin_account.multilogin_email = email
                        multilogin_account.multilogin_password = password
                        multilogin_account.multilogin_token = token
                        multilogin_account.multilogin_folder_id = profile.get('folder_id', '')
                        # multilogin_account.multilogin_profile_id = profile.get('id', '')
                        multilogin_account.multilogin_profile_name = profile.get('name', '')
                        multilogin_account.save()

                messages.success(request, 'Đăng nhập Multilogin thành công!')
                return redirect('user')
            else:
                messages.error(request, 'Đăng nhập Multilogin thất bại. Vui lòng kiểm tra lại thông tin.')
    else:
        form = MultiLoginForm()
    return render(request, 'multilogin.html', {'form': form})

def run_script(request, func):  
    multilogin_accounts = MultiloginAccount.objects.filter(user=request.user).values()
    email = multilogin_accounts[0]['multilogin_email'] if multilogin_accounts else ''
    password = multilogin_accounts[0]['multilogin_password'] if multilogin_accounts else ''
    signin(email, password)
    profile_id = request.GET['profile_id']
    folder_id = multilogin_accounts[0]['multilogin_folder_id']
    host = request.GET['host']
    start = datetime.datetime.now()
    driver = multiloginSetDriver(profile_id, folder_id, host)
    driver.get('https://www.google.com')
    try:
        func = globals()[func]
        func(driver)
    except Exception as e:
        print("Error (stack):", e)
    multiloginDestroyDriver(profile_id)
    end = datetime.datetime.now()
    executionTime = end - start

    print("Start time - " + str(start))
    print("End time - " + str(end))
    print("Execution Time - " + str(executionTime))