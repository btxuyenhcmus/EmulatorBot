import time


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
