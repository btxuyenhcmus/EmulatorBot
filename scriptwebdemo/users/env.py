from dotenv import load_dotenv
import os

load_dotenv()


CHROME_PATH = "/home/btxuyen/.wdm/drivers/chromedriver/linux64/119.0.6045.105/chromedriver"
CHROME_USER_PROFILE = "/home/btxuyen/testprofile2"

MLX_BASE = os.environ.get('MLX_BASE')
MLX_LAUNCHER = os.environ.get('MLX_LAUNCHER')
LOCALHOST = os.environ.get('MLX_LOCALHOST')

USERNAME = os.environ.get('MLX_USERNAME')
PASSWORD = os.environ.get('MLX_PASSWORD')
