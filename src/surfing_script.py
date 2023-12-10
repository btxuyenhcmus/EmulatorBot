from selenium.webdriver.common.keys import Keys

import time
import random


def search_google(driver, text):
    print("Search Google Starting...")
    search_box = driver.find_element("name", "q")
    for char in text:
        search_box.send_keys(char)
        time.sleep(0.3)

    search_box.send_keys(Keys.RETURN)

    driver.implicitly_wait(5)
    print("Search Google Ended!")


def scroll_smooth_to_end(driver):
    print("Scroll to end starting...")
    height = int(driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"))
    # Set the initial scroll position
    scroll_position = 0

    # Define the step size for smooth scrolling
    step = 10

    while scroll_position < height:
        # Scroll down by the defined step size
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        # Increment the scroll position
        scroll_position += step

        # Wait for a short time to create a smooth scrolling effect
        time.sleep(0.1)
    print("Scroll to end ended!")


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


def scroll_smooth_to_top(driver):
    print("Scroll to top starting...")
    # Set the initial scroll position to the bottom of the page
    scroll_position = int(driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"))

    # Define the step size for smooth scrolling
    step = -10  # Negative step to scroll up

    while scroll_position > 0:
        # Scroll up by the defined step size
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        # Decrement the scroll position
        scroll_position += step

        # Wait for a short time to create a smooth scrolling effect
        time.sleep(0.1)
    print("Scroll to top ended!")


def click_random_top_result(driver):
    driver.implicitly_wait(5)
    result_links = driver.find_elements_by_tag_name('h3')
    random_link = result_links[random.randint(0, 5)]
    random_link.click()
    time.sleep(10)


def click_random_page(driver):
    driver.implicitly_wait(5)
    all_links = driver.find_elements_by_tag_name("a")
    all_links[random.randint(0, 100)].click()
    time.sleep(10)


def surfing(driver):
    print("Surfing web starting...")
    driver.implicitly_wait(5)
    driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
    time.sleep(5)
    scroll_smooth_to_end(driver)
    scroll_smooth_to_top(driver)
    print("Surfing web ended!")


def surfing_script_run(driver):
    search_google(driver, "macys shoes tommy")
    scroll_smooth_to_end(driver)
    scroll_smooth_to_top(driver)
    click_random_top_result(driver)
    surfing(driver)
    click_random_page(driver)
    surfing(driver)
    click_random_page(driver)
    surfing(driver)
    click_random_page(driver)
    surfing(driver)
