from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time

class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        """Find element by locator."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator, timeout: int = 5):
        """Find elements by locator with optional wait."""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def click_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
            element.click()
        except ElementClickInterceptedException:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def send_keys_to_element(self, locator, text):
        """Send keys to element by locator."""
        self.clear_and_send_keys(locator, text)

    def clear_and_send_keys(self, locator, text):
        element = self.find_element(locator)
        
        element.clear()
        
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        
        # Bước 3: Gõ chữ mới vào
        element.send_keys(text)