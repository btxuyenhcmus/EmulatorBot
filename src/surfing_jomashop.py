from selenium.webdriver.common.keys import Keys

import time
import random


def scroll_smooth_to_medium(driver, height=None):
    print("Scroll to medium starting...")
    height = height or int(driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);") / 2)
    # Set the initial scroll position
    scroll_position = 0

    # Define the step size for smooth scrolling
    step = 20

    while scroll_position < height:
        # Scroll down by the defined step size
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        # Increment the scroll position
        scroll_position += step

        # Wait for a short time to create a smooth scrolling effect
        time.sleep(0.1)
    print("Scroll to end ended!")


def scroll_smooth_to_top(driver, height=None):
    print("Scroll to top starting...")
    # Set the initial scroll position to the bottom of the page
    scroll_position = height or int(driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);") / 2)

    # Define the step size for smooth scrolling
    step = -20  # Negative step to scroll up

    while scroll_position > 0:
        # Scroll up by the defined step size
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        # Decrement the scroll position
        scroll_position += step

        # Wait for a short time to create a smooth scrolling effect
        time.sleep(0.1)
    print("Scroll to top ended!")


def add_to_bag_product(driver):
    driver.implicitly_wait(5)
    menuitems = driver.find_elements_by_css_selector(".menu-item-header")
    random.choice(menuitems).click()
    time.sleep(5)

    scroll_smooth_to_medium(driver, 500)
    time.sleep(5)

    products = driver.find_elements_by_css_selector("li.productItem")
    products[random.randint(0, 20)].click()
    time.sleep(5)

    scroll_smooth_to_medium(driver, 400)
    time.sleep(5)

    add_cart_btn = driver.find_element_by_css_selector(
        "button.add-to-cart-btn")
    add_cart_btn.click()
    time.sleep(7)

    close_btn = driver.find_element_by_css_selector("button.btn-close")
    close_btn.click()
    time.sleep(2)


def clear_cart(driver):
    rhs = driver.find_elements_by_css_selector(".center-content span.rhs-item")
    cart_btn = rhs[-1]
    cart_btn.click()
    time.sleep(5)

    remove_buttons = driver.find_elements_by_css_selector(
        ".cart-item-action span.cart-item-remove")
    while len(remove_buttons) != 0:
        remove_buttons[0].click()
        time.sleep(2)

        yes_btn = driver.find_elements_by_css_selector(
            ".modal-dialog .modal-footer button")[1]
        yes_btn.click()
        time.sleep(7)
        remove_buttons = driver.find_elements_by_css_selector(
            ".cart-item-action span.cart-item-remove")

    close_btn = driver.find_element_by_css_selector("button.btn-close")
    close_btn.click()


def surfing_jomashop_run(driver):
    driver.get('https://www.jomashop.com')
    driver.implicitly_wait(15)
    driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
    scroll_smooth_to_medium(driver)
    scroll_smooth_to_top(driver)
    add_to_bag_product(driver)
    time.sleep(5)