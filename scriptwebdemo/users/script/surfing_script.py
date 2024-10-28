from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .utils import scroll_smooth_to_top, scroll_smooth_to_end

import time
import random


def search_google(driver, text):
    print("Search Google Starting...")
    search_box = driver.find_element(By.NAME, "q")
    for char in text:
        search_box.send_keys(char)
        time.sleep(0.3)

    search_box.send_keys(Keys.RETURN)

    driver.implicitly_wait(5)
    print("Search Google Ended!")


def click_random_top_result(driver):
    driver.implicitly_wait(5)
    result_links = driver.find_elements(By.TAG_NAME, 'h3')
    random_link = result_links[random.randint(0, 5)]
    random_link.click()
    time.sleep(10)


def click_random_page(driver):
    driver.implicitly_wait(5)
    all_links = driver.find_elements(By.TAG_NAME, "a")
    all_links[random.randint(0, 100)].click()
    time.sleep(10)


def surfing(driver):
    print("Surfing web starting...")
    driver.implicitly_wait(5)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    time.sleep(5)
    scroll_smooth_to_end(driver)
    scroll_smooth_to_top(driver, step=-10)
    print("Surfing web ended!")


def surfing_script_run(driver):
    search_google(driver, "macys shoes tommy")
    scroll_smooth_to_end(driver, step=10)
    scroll_smooth_to_top(driver, step=-10)
    click_random_top_result(driver)
    surfing(driver)
    click_random_page(driver)
    surfing(driver)
    click_random_page(driver)
    surfing(driver)
    click_random_page(driver)
    surfing(driver)
