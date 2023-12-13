from selenium import webdriver
from env import CHROME_PATH, CHROME_USER_PROFILE


def setDriver():
    # Initializing Chrome Options from the Webdriver
    options = webdriver.ChromeOptions()
    prefs = {"profile.password_manager_enabled": False,
             "credentials_enable_service": False, "useAutomationExtension": False}
    options.add_experimental_option("prefs", prefs)
    # Adding Argument to Not Use Automation Extension
    options.add_experimental_option("useAutomationExtension", False)
    # Excluding enable-automation Switch
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("start-fullscreen")
    options.add_argument("disable-popup-blocking")
    options.add_argument("disable-notifications")
    options.add_argument("disable-gpu")  # renderer timeout
    options.add_argument(f"--user-data-dir={CHROME_USER_PROFILE}")

    driver = webdriver.Chrome(CHROME_PATH, options=options)
    driver.set_page_load_timeout(10)

    return driver
