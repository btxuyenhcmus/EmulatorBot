import time
import inspect
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class WebAutomation:
    def __init__(self, driver):
        self.driver = driver

    @classmethod
    def get_action_list(cls):
        action_list = []
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if not name.startswith('__') and name != "get_action_list":
                docstring = method.__doc__
                if docstring:
                    action_name = ""
                    for line in docstring.split("\n"):
                        if "Action:" in line:
                            action_name = line.replace("Action:", "").strip()
                            break

                    params = []
                    capture_params = False
                    for line in docstring.split("\n"):
                        if "Parameters:" in line:
                            capture_params = True
                            continue
                        if capture_params:
                            if ":" not in line or not line.strip():
                                break
                            param_name = line.split(":")[0].strip()
                            params.append(param_name)
                    action_list.append({
                        'name': action_name,
                        'params': params,
                        "method_name": name,
                    })
        return action_list

    def open_url(self, *args, **kwargs):
        """
        Action: Truy cập web

        Parameters:
        url: địa chỉ web
        """
        print("Start search " + kwargs['url'])
        self.driver.get(kwargs['url'])
        time.sleep(int(kwargs["delay"]))

    def watch_video(self, *args, **kwargs):
        """
        Action: Xem video

        Parameters:
        url: địa chỉ video

        """
        print("Start watch video " + kwargs['url'])
        self.driver.implicitly_wait(5)
        self.driver.get(kwargs['url'])
        self.click_element(
            self.driver, css_selector='button.ytp-play-button')
        time.sleep(int(kwargs["delay"]))

    def click_element(self, *args, **kwargs):
        """
        Action: Click vào phần tử trên trang

        Parameters:
        selector: css selector của phần tử đó

        """
        ActionChains(self.driver).click(self.driver.find_element(
            By.CSS_SELECTOR, kwargs['selector'])).perform()
        time.sleep(int(kwargs["delay"]))

    def scroll_to_element(self, *args, **kwargs):
        """
        Action: Cuộn đến phần tử trên trang

        Parameters:
        selector: css selector của phần tử đó
        """
        element = self.driver.find_element(By.CSS_SELECTOR, kwargs['selector'])
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        print("Scroll to element " + kwargs['selector'])
        time.sleep(int(kwargs["delay"]))

    def refresh_page(self, *args, **kwargs):
        """
        Action: Refresh trang

        Description:
        Refresh trang
        """
        self.driver.refresh()
        time.sleep(int(kwargs["delay"]))
        print("Refresh page")

    def navigate_back(self, *args, **kwargs):
        """
        Action: Trở lại trang trước đó

        Description:
        Trở lại trang trước đó
        """
        self.driver.back()
        time.sleep(int(kwargs["delay"]))

    def navigate_forward(self, *args, **kwargs):
        """
        Action: Đến trang tiếp theo

        Description:
        Đến trang tiếp theo
        """
        self.driver.forward()
        time.sleep(int(kwargs["delay"]))

    def scroll_smooth_to_medium(self, *args, **kwargs):
        """
        Action: Cuộn đến giữa trang

        Description:
        Cuộn đến giữa trang
        """
        print("Scroll to medium starting...")
        height = height or int(self.driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);") / 2)
        # Set the initial scroll position
        scroll_position = 0

        while scroll_position < height:
            # Scroll down by the defined step size
            self.driver.execute_script(
                f"window.scrollTo(0, {scroll_position});")

            # Increment the scroll position
            scroll_position += 20

            # Wait for a short time to create a smooth scrolling effect
            time.sleep(0.1)
        time.sleep(int(kwargs["delay"]))
        print("Scroll to end ended!")

    def scroll_smooth_to_end(self, *args, **kwargs):
        """
        Action: Cuộn đến cuối trang

        """
        print("Scroll to end starting...")
        height = int(self.driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"))
        # Set the initial scroll position
        scroll_position = 0

        while scroll_position < height:
            # Scroll down by the defined step size
            self.driver.execute_script(
                f"window.scrollTo(0, {scroll_position});")

            # Increment the scroll position
            scroll_position += 20

            # Wait for a short time to create a smooth scrolling effect
            time.sleep(0.1)
        time.sleep(int(kwargs["delay"]))
        print("Scroll to end ended!")

    def scroll_smooth_to_top(self, *args, **kwargs):
        """
        Action: Cuộn đến đầu trang

        """
        print("Scroll to top starting...")
        height = None
        # Set the initial scroll position to the bottom of the page
        scroll_position = height or int(self.driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);") / 2)

        while scroll_position > 0:
            # Scroll up by the defined step size
            self.driver.execute_script(
                f"window.scrollTo(0, {scroll_position});")

            # Decrement the scroll position
            scroll_position += -20

            # Wait for a short time to create a smooth scrolling effect
            time.sleep(0.1)
        time.sleep(int(kwargs["delay"]))
        print("Scroll to top ended!")
