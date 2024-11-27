from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Script, ScriptStep
from ..multilogin.models import MultiloginAccount
from ..multilogin.multilogindriver import setDriver as multiloginSetDriver, stop_profile as multiloginDestroyDriver, signin
import datetime
import time
import json
from ..actions.actions import WebAutomation


def create_script(request):
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            script_id = data.get('scriptId')
            script_name = data.get('scriptName')
            steps = data.get('steps')

            if script_id:
                script = Script.objects.get(id=script_id, user=request.user)
                script.name = script_name
                script.save()
                ScriptStep.objects.filter(
                    script=script).delete()
            else:
                script = Script.objects.create(
                    name=script_name, user=request.user)

            for step in steps:
                new_script_step = ScriptStep.objects.create(
                    script=script,
                    action=step['action'],
                    step_order=step['step_order'],
                    parameters=step['parameters']
                )
                new_script_step.save()
            return JsonResponse({'status': 'success', }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def get_script(request):
    scripts_info = []
    scripts = Script.objects.filter(user=request.user)
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


def get_script_by_id(request, script_id):
    script = Script.objects.get(id=script_id, user=request.user)
    if script:
        steps = ScriptStep.objects.filter(script=script).order_by('step_order')

        steps_data = [
            {
                'step_order': step.step_order,
                'action': step.action,
                'parameters': step.parameters,
            }
            for step in steps
        ]

        script_data = {
            'id': script.id,
            'name': script.name,
            'steps': steps_data,
        }

        return JsonResponse({'success': True, 'script': script_data}, status=200)
    else:
        return JsonResponse({'success': False, 'message': 'Script not found'}, status=404)


def fetch_scripts(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            scripts = get_script(request)
            return JsonResponse({'scripts': scripts})
        return JsonResponse({'error': 'User not authenticated'}, status=401)


def run_script(request, script_id):
    multilogin_accounts = MultiloginAccount.objects.filter(
        user=request.user).values()
    email = multilogin_accounts[0]['email'] if multilogin_accounts else ''
    password = multilogin_accounts[0]['password'] if multilogin_accounts else ''
    token = signin(email, password)
    host = request.GET['host']
    profile_id = request.GET['profile_id']
    folder_id = multilogin_accounts[0]['folder_id']
    start = datetime.datetime.now()
    driver = multiloginSetDriver(profile_id, folder_id, host, token)
    driver.get('https://www.google.com')
    try:
        scriptSteps = ScriptStep.objects.filter(
            script_id=script_id
        ).order_by('step_order')
        web_automation = WebAutomation(driver)
        for scriptStep in scriptSteps:
            if hasattr(web_automation, scriptStep.action):
                print(scriptStep.parameters)
                getattr(web_automation, scriptStep.action)(
                    **scriptStep.parameters)
            else:
                print(
                    f"Method {scriptStep.action} not found in WebAutomation.")

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


def delete_script(request, script_id):
    if request.method == "POST":
        try:
            script = get_object_or_404(Script, id=script_id, user=request.user)
            script.steps.all().delete()
            script.delete()
            return JsonResponse({'success': True, 'message': 'Delete script success'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Unsupport'})
