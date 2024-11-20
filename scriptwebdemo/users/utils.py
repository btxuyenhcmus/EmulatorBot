import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def search_google(driver, url):
    print("Start search " + url)
    driver.get(url)


def watch_video(driver, url):
    print("Start watch video " + url)
    driver.implicitly_wait(5)
    driver.get(url)
    click_using_css_selector(
        driver, css_selector='button.ytp-play-button')


def click_using_css_selector(driver, css_selector):
    element = driver.find_element(By.CSS_SELECTOR, css_selector)
    ActionChains(driver).click(element).perform()


def click_position(driver, x, y):
    driver.execute_script(f"window.scrollTo({x}, {y});")
    time.sleep(1)
    action = ActionChains(driver)
    action.move_by_offset(x, y).click().perform()
    action.move_by_offset(-x, -y).click().perform()
    print('click at position ', x, y)


def scroll_down(driver, pixels):
    print(f'Scroll down {pixels} starting')
    current_scroll_position = driver.execute_script("return window.scrollY;")

    target_scroll_position = current_scroll_position + int(pixels)

    while current_scroll_position < target_scroll_position:
        driver.execute_script(
            f"window.scrollTo(0, {current_scroll_position});")

        current_scroll_position += 10

        if current_scroll_position > target_scroll_position:
            current_scroll_position = target_scroll_position

        time.sleep(0.1)

    print("Scroll down ended!")


def scroll_up(driver, pixels):
    print(f'Scroll up {pixels} starting')
    current_scroll_position = driver.execute_script("return window.scrollY;")

    target_scroll_position = max(0, current_scroll_position - pixels)

    while current_scroll_position > target_scroll_position:
        driver.execute_script(
            f"window.scrollTo(0, {current_scroll_position});")

        current_scroll_position -= 20

        if current_scroll_position < target_scroll_position:
            current_scroll_position = target_scroll_position

        time.sleep(0.1)

    print("Scroll up ended!")


def scroll_smooth_to_medium(driver, height=None, step=20):
    print("Scroll to medium starting...")
    height = height or int(driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);") / 2)
    # Set the initial scroll position
    scroll_position = 0

    while scroll_position < height:
        # Scroll down by the defined step size
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        # Increment the scroll position
        scroll_position += step

        # Wait for a short time to create a smooth scrolling effect
        time.sleep(0.1)
    print("Scroll to end ended!")


def scroll_smooth_to_end(driver, step=20):
    print("Scroll to end starting...")
    height = int(driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"))
    # Set the initial scroll position
    scroll_position = 0

    while scroll_position < height:
        # Scroll down by the defined step size
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        # Increment the scroll position
        scroll_position += step

        # Wait for a short time to create a smooth scrolling effect
        time.sleep(0.1)
    print("Scroll to end ended!")


def scroll_smooth_to_top(driver, height=None, step=-20):
    print("Scroll to top starting...")
    # Set the initial scroll position to the bottom of the page
    scroll_position = height or int(driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);") / 2)

    while scroll_position > 0:
        # Scroll up by the defined step size
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")

        # Decrement the scroll position
        scroll_position += step

        # Wait for a short time to create a smooth scrolling effect
        time.sleep(0.1)
    print("Scroll to top ended!")
