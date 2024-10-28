from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from .utils import scroll_smooth_to_top, scroll_smooth_to_medium

import time
import random


def add_to_bag_product(driver):
    driver.implicitly_wait(5)
    menuitems = driver.find_elements(By.CSS_SELECTOR, "ul#mainNavigationFobs li")
    menuitems[random.randint(0, 6)].click()
    time.sleep(5)

    scroll_smooth_to_medium(driver, 200)
    time.sleep(5)

    products = driver.find_elements(By.CSS_SELECTOR, ".product-pool-media-carousel .productDetail .productDescription a")
    if len(products) == 0:
        categories = driver.find_elements(By.CSS_SELECTOR, "#row_1 .aem-icon-div")
        random.choice(categories).click()
        time.sleep(5)
        products = driver.find_elements(By.CSS_SELECTOR, "li.productThumbnailItem")

    random.choice(products).click()
    time.sleep(5)

    if len(driver.window_handles) > 1:
        driver.switch_to_window(driver.window_handles[-1])

    size_selector = driver.find_elements(By.CSS_SELECTOR, '[data-el="sizes"] ul li')
    if size_selector:
        random.choice(size_selector).click()

    add_cart_btn = driver.find_element(By.CSS_SELECTOR, '[data-el="call-to-action"] button[data-action="product:bag:add"]')
    add_cart_btn.click()
    time.sleep(10)

    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)


def surfing_macys_run(driver):
    driver.get('https://macys.com')
    driver.implicitly_wait(10)
    scroll_smooth_to_medium(driver)
    scroll_smooth_to_top(driver)
    time.sleep(5)
    add_to_bag_product(driver)
