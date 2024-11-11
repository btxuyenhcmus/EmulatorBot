from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, MultiLoginForm
from .models import MultiloginAccount, Action, Script, ScriptStep
from .multilogindriver import signin, profile_search
from django.contrib import messages
import datetime
import sys
import json
from .multilogindriver import setDriver as multiloginSetDriver, stop_profile as multiloginDestroyDriver
from .utils import *


def home(request):
    user = request.user
    scripts = get_script(user)
    print(scripts)
    multilogin_accounts = []
    if user.is_authenticated:
        multilogin_accounts = MultiloginAccount.objects.filter(
            user=request.user).values()
        actions = Action.objects.all().values()

    return render(request, 'home.html', {'scripts': scripts, 'multilogin_accounts': multilogin_accounts, 'actions': actions})


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
    multilogin_accounts = MultiloginAccount.objects.filter(
        user=request.user).values()
    email = multilogin_accounts[0]['multilogin_email'] if multilogin_accounts else ''
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
                        multilogin_account.multilogin_folder_id = profile.get(
                            'folder_id', '')
                        # multilogin_account.multilogin_profile_id = profile.get('id', '')
                        multilogin_account.multilogin_profile_name = profile.get(
                            'name', '')
                        multilogin_account.save()

                messages.success(request, 'Login success')
                return redirect('user')
            else:
                messages.error(
                    request, 'Login failed. Please check infomation again')
    else:
        form = MultiLoginForm()
    return render(request, 'multilogin.html', {'form': form})


def create_script(request):
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            script_name = data.get('scriptName')
            steps = data.get('steps')
            new_script = Script.objects.create(
                name=script_name, user=request.user)
            new_script.save()
            for step in steps:
                new_script_step = ScriptStep.objects.create(
                    script=new_script,
                    action=Action.objects.get(pk=step['action_id']),
                    step_order=step['step_order'],
                    parameters=step['parameters']
                )
                new_script_step.save()
            return JsonResponse({'status': 'success', }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def get_script(user):
    scripts_info = []
    scripts = Script.objects.filter(user=user)
    for script in scripts:
        steps = ScriptStep.objects.filter(script=script)
        script_info = {
            'id': script.id,
            'name':  script.name,
            'steps':  []
        }
        for step in steps:
            script_info['steps'].append({
                'step_order': step.step_order,
                'action': step.action,
                'parameters': step.parameters,
                'created': step.created.strftime("%d/%m/%Y")

            })

        scripts_info.append(script_info)
    return scripts_info


def run_script(request, scriptId):
    multilogin_accounts = MultiloginAccount.objects.filter(
        user=request.user).values()
    email = multilogin_accounts[0]['multilogin_email'] if multilogin_accounts else ''
    password = multilogin_accounts[0]['multilogin_password'] if multilogin_accounts else ''
    token = signin(email, password)
    profile_id = request.GET['profile_id']
    folder_id = multilogin_accounts[0]['multilogin_folder_id']
    # token = multilogin_accounts[0]['multilogin_token']
    host = request.GET['host']
    start = datetime.datetime.now()
    driver = multiloginSetDriver(profile_id, folder_id, host, token)
    driver.get('https://www.google.com')
    try:
        scriptSteps = ScriptStep.objects.filter(
            script_id=scriptId
        ).order_by('step_order')

        action_handlers = {
            'visit_website': lambda scriptStep, func: func(
                driver,
                scriptStep.parameters['url']
            ) or time.sleep(int(scriptStep.parameters['delay'])),

            'scroll_up': lambda scriptStep, func: func(
                driver,
                scriptStep.parameters['amount']
            ) or time.sleep(int(scriptStep.parameters['delay'])),

            'scroll_down': lambda scriptStep, func: func(
                driver,
                scriptStep.parameters['amount']
            ) or time.sleep(int(scriptStep.parameters['delay'])),

            'scroll_start': lambda scriptStep, func: func(driver)
            or time.sleep(int(scriptStep.parameters['delay'])),

            'scroll_end': lambda scriptStep, func: func(driver)
            or time.sleep(int(scriptStep.parameters['delay'])),

            'watch_video': lambda scriptStep, func: func(
                driver,
                scriptStep.parameters['url']
            ) or time.sleep(int(scriptStep.parameters['delay'])),

            'click_position': lambda scriptStep, func: func(
                driver,
                int(scriptStep.parameters['x_position']),
                int(scriptStep.parameters['y_position'])
            ) or time.sleep(int(scriptStep.parameters['delay'])),
        }

        for scriptStep in scriptSteps:
            action = Action.objects.get(id=scriptStep.action_id)
            func = globals()[action.action_func]
            handler = action_handlers.get(action.action_type)
            if handler:
                handler(scriptStep, func)
            else:
                raise ValueError(f"Unsupported action type: {
                                 action.action_type}")
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        multiloginDestroyDriver(profile_id, token)
        end = datetime.datetime.now()
        executionTime = end - start

    return JsonResponse({
        'status': 'success',
        'start_time': str(start),
        'end_time': str(end),
        'execution_time': str(executionTime)
    })
