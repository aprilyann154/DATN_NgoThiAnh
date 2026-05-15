import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

class BasePage:
    # FIX: Tăng timeout mặc định từ 5 lên 15 giây
    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.DEFAULT_TIMEOUT)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def click_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            time.sleep(0.2)
            element.click()
        except Exception:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def send_keys_to_element(self, locator, text):
        self.clear_and_send_keys(locator, text)

    def clear_and_send_keys(self, locator, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(text)
        except Exception:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].value = '';", element)
            element.send_keys(text)

    def wait_for_page_ready(self, timeout: int = 15) -> None:
        """Chờ document.readyState == complete."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )