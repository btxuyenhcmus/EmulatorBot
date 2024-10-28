from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .utils import scroll_smooth_to_top, scroll_smooth_to_medium

import time
import random


def search_products_add_to_cart(driver, text):
    search_box = driver.find_element("name", "_nkw")
    for char in text:
        search_box.send_keys(char)
        time.sleep(0.3)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    products = driver.find_elements(By.CSS_SELECTOR, ".s-item__info a")
    product = random.choice(products)
    scroll_smooth_to_medium(driver, product.location['y'])
    product.click()
    time.sleep(5)

    add_cart_btn = driver.find_element(
        By.CSS_SELECTOR, "span.ux-call-to-action__cell")
    add_cart_btn.click()
    time.sleep(2)

def surfing_root_add_to_cart(driver):
    categories = driver.find_elements(
        By.CSS_SELECTOR, "ul.hl-popular-destinations-elements li")
    if len(categories) > 0:
        random.choice(categories).click()
        time.sleep(5)

        scroll_smooth_to_medium(driver, 500)
        time.sleep(5)

        products = driver.find_elements(By.XPATH, '//*[@role="listitem"]')
        products[3].click()
        time.sleep(5)
    else:
        categories = driver.find_elements(
            By.CSS_SELECTOR, "div.vl-popular-destinations--evo-v1__elements li")
        categories[random.randint(0, 7)].click()
        time.sleep(5)

    scroll_smooth_to_medium(driver, 600)
    time.sleep(5)

    products = driver.find_elements(
        By.CSS_SELECTOR, "ul.brwrvr__item-results li div.brwrvr__item-card__image-wrapper")
    products[random.randint(0, 10)].click()
    time.sleep(5)

    add_cart_btn = driver.find_element(
        By.CSS_SELECTOR, "span.ux-call-to-action__cell")
    add_cart_btn.click()
    time.sleep(2)


def add_to_bag_product(driver):
    driver.implicitly_wait(5)
    surfing_root_add_to_cart(driver)
    search_products_add_to_cart(driver, "Shoes")


def surfing_ebay_run(driver):
    driver.get('https://www.ebay.com')
    driver.implicitly_wait(10)
    scroll_smooth_to_medium(driver)
    scroll_smooth_to_top(driver)
    add_to_bag_product(driver)
