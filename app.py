from flask import Flask, render_template, request
from drivers.multilogindriver import profile_search, signin
import subprocess

app = Flask(__name__)

# Sample list of scripts
scripts = [
    {
        'name': 'Tìm kiếm theo keywords',
        'func': 'surfing_script_run'
    },
    {
        'name': 'Lướt web macys',
        'func': 'surfing_macys_run'
    },
    {
        'name': 'Lướt web jomashop',
        'func': 'surfing_jomashop_run'
    },
    {
        'name': 'Lướt web ebay',
        'func': 'surfing_ebay_run'
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
    try:
        profiles = profile_search()
    except Exception as e:
        profiles = []
    return render_template('index.html', scripts=scripts, profiles=profiles)


@app.route('/run/<func>')
def run_script(func):
    args = request.args
    profile_id = args['profile']
    folder_id = args['folder']
    subprocess.call(
        ['python3', 'main.py', func, profile_id, folder_id], bufsize=0)
    return 'Done 1 script on background.'


@app.route('/refresh')
def refresh():
    signin()
    return 'Refresh done.'


if __name__ == '__main__':
    app.run(debug=True)
