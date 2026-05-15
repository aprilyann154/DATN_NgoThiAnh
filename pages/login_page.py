from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class LoginPage(BasePage):

    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.ID, "pwdInput")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert.alert-danger")
    DASHBOARD = (By.ID, "dashboard") 
    
    SIGNUP_LINK = (By.XPATH, "//a[@href='/register']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[@href='/forgot-password']")

    def __init__(self, driver, base_url: str = "http://localhost:3000"):
        super().__init__(driver)
        self.url = f"{base_url.rstrip('/')}/login"

    def load(self):
        self.driver.get(self.url)
        
        self.driver.delete_all_cookies()
    
        self.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")

        self.driver.refresh()
        
        if "/login" not in self.driver.current_url:
            self.driver.get(self.url)
            
        time.sleep(0.5)

    def login(self, username, password):
        """Thực hiện điền form và nhấn Đăng nhập."""
        if username:
            self.send_keys_to_element(self.USERNAME_FIELD, username)
        if password:
            self.send_keys_to_element(self.PASSWORD_FIELD, password)
            
        self.click_element(self.LOGIN_BUTTON)
        time.sleep(1) 

    def load_and_login(self, username, password):
        self.load()
        self.login(username, password)

    def get_error_message(self):
        try:
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return element.text
        except TimeoutException:
            return None

    def is_login_successful(self):
        try:
            self.wait.until(lambda driver: "/login" not in driver.current_url)
            return True
        except TimeoutException:
            return False

    def click_signup_link(self):
        self.click_element(self.SIGNUP_LINK)

    def click_forgot_password_link(self):
        self.click_element(self.FORGOT_PASSWORD_LINK)

    def is_on_signup_page(self):
        try:
            self.wait.until(lambda driver: "/signup" in driver.current_url.lower() or "/register" in driver.current_url.lower())
            return True
        except TimeoutException:
            return False

    def is_on_forgot_password_page(self):
        try:
            self.wait.until(lambda driver: "forgot" in driver.current_url.lower() or "reset" in driver.current_url.lower())
            return True
        except TimeoutException:
            return False