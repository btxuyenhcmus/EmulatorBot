from selenium import webdriver
from .env import MLX_BASE, MLX_LAUNCHER, LOCALHOST
import hashlib
import requests
import json


HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def signin(email:str, password: str) -> str:
    payload = {
        'email': email,
        'password': hashlib.md5(password.encode()).hexdigest()
    }

    r = requests.post(f'{MLX_BASE}/user/signin', json=payload)

    if (r.status_code != 200):
        print(f'\nError during login: {r.text}\n')
        return None

    response = r.json()['data']

    token = response['token']
    print(f'MultiloginX token: {token}')
    HEADERS.update({"Authorization": f'Bearer {token}'})

    return token


def profile_search():
    body = {"offset": 0, "limit": 10, "search_text": "", "tags": [
    ], "storage_type": "all", "is_removed": False, "order_by": "created_at", "sort": "desc"}
    r = requests.post(f'{MLX_BASE}/pss/search',
    headers=HEADERS, data=json.dumps(body))
    response = r.json()
    print(response)
    return response.get('data').get('profiles', [])


def start_profile(ChromiumOptions, profile_id, folder_id,host) -> webdriver:
    r = requests.get(
        f'{MLX_LAUNCHER}/profile/f/{folder_id}/p/{profile_id}/start?automation_type=selenium', headers=HEADERS)

    response = r.json()

    if (r.status_code != 200):
        print(f'\nError while starting profile: {r.text}\n')
    else:
        print(f'\nProfile {profile_id} started.\n')
        selenium_port = response.get('data').get('port')
        driver = webdriver.Remote(
            command_executor=f'{host}:{selenium_port}', options=ChromiumOptions)
        return driver


def stop_profile(profile_id) -> None:
    r = requests.get(
        f'{MLX_LAUNCHER}/profile/stop/p/{profile_id}', headers=HEADERS)

    if (r.status_code != 200):
        print(f'\nError while stopping profile: {r.text}\n')
    else:
        print(f'\nProfile {profile_id} stopped.\n')


def setDriver(profile_id, folder_id, host):
    # Initializing Chrome Options from the Webdriver
    options = webdriver.ChromeOptions()

    driver = start_profile(options, profile_id, folder_id,host)
    driver.maximize_window()
    return driver
