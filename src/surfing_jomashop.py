from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .utils import scroll_smooth_to_top, scroll_smooth_to_medium

import time
import random


def close_popup(driver):
    try:
        popup = driver.find_element(By.ID, "ltkpopup-content")
        if popup:
            popupClose = driver.find_element(By.CLASS_NAME, "ltkpopup-close")
            popupClose.click()
    except:
        pass


def add_to_bag_product(driver):
    driver.implicitly_wait(5)
    menuitems = driver.find_elements(By.CSS_SELECTOR, ".menu-item-header")
    random.choice(menuitems).click()
    time.sleep(5)

    scroll_smooth_to_medium(driver, 500)
    time.sleep(5)

    products = driver.find_elements(By.CSS_SELECTOR, "li.productItem")
    products[random.randint(0, 20)].click()
    time.sleep(5)

    scroll_smooth_to_medium(driver, 400)
    time.sleep(5)

    add_cart_btn = driver.find_element(
        By.CSS_SELECTOR, "button.add-to-cart-btn")
    add_cart_btn.click()
    time.sleep(7)

    close_btn = driver.find_element(By.CSS_SELECTOR, "button.btn-close")
    close_btn.click()
    time.sleep(2)


def clear_cart(driver):
    rhs = driver.find_element(By.CSS_SELECTOR, ".center-content span.rhs-item")
    cart_btn = rhs[-1]
    cart_btn.click()
    time.sleep(5)

    remove_buttons = driver.find_element(
        By.CSS_SELECTOR, ".cart-item-action span.cart-item-remove")
    while len(remove_buttons) != 0:
        remove_buttons[0].click()
        time.sleep(2)

        yes_btn = driver.find_element(
            By.CSS_SELECTOR, ".modal-dialog .modal-footer button")[1]
        yes_btn.click()
        time.sleep(7)
        remove_buttons = driver.find_element(
            By.CSS_SELECTOR, ".cart-item-action span.cart-item-remove")

    close_btn = driver.find_element(By.CSS_SELECTOR, "button.btn-close")
    close_btn.click()


def surfing_jomashop_run(driver):
    driver.get('https://www.jomashop.com')
    driver.implicitly_wait(10)
    close_popup(driver)
    scroll_smooth_to_medium(driver)
    close_popup(driver)
    scroll_smooth_to_top(driver)
    close_popup(driver)
    add_to_bag_product(driver)
    time.sleep(5)
