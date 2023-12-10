from flask import Flask, render_template, request
from drivers.multilogindriver import profile_search
import subprocess

app = Flask(__name__)

# Sample list of scripts
scripts = [
    {
        'name': 'Tìm kiếm theo keywords',
        'func': 'surfing_script_run'
    },
    {
        'name': 'Lướt web jomashop',
        'func': 'surfing_jomashop_run'
    },
    {
        'name': 'Chơi game 2048',
        'func': 'game_run'
    },
    {
        'name': 'Đọc báo trên Fox',
        'func': 'fox_news_run'
    }
]


@app.route('/')
def index():
    profiles = profile_search()
    return render_template('index.html', scripts=scripts, profiles=profiles)


@app.route('/run/<script_name>')
def run_script(script_name):
    script_path = 'main.py'
    if script_path:
        subprocess.Popen(['python3', script_path], bufsize=0)
        return f'Started running {script_name} in the background.'
    else:
        return f'Script {script_name} not found.'


@app.route('/runv1/<func>')
def runv1_script(func):
    args = request.args
    profile_id = args['profile']
    folder_id = args['folder']
    subprocess.call(
        ['python3', 'main.py', func, profile_id, folder_id], bufsize=0)
    return 'Done 1 script on background.'


if __name__ == '__main__':
    app.run(debug=True)
