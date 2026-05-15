from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        # FIX: Xóa cookies TRƯỚC khi load trang, không refresh lần 2
        try:
            self.driver.delete_all_cookies()
            self.driver.execute_script(
                "window.localStorage.clear(); window.sessionStorage.clear();"
            )
        except Exception:
            pass

        self.driver.get(self.url)

        # FIX: Chờ page load thật sự thay vì sleep cố định
        self.wait_for_page_ready()

        # Nếu bị redirect đi đâu đó (đang còn session cũ), load lại
        if "/login" not in self.driver.current_url:
            try:
                self.driver.delete_all_cookies()
                self.driver.execute_script(
                    "window.localStorage.clear(); window.sessionStorage.clear();"
                )
            except Exception:
                pass
            self.driver.get(self.url)
            self.wait_for_page_ready()

    def login(self, username, password):
        """Điền form và nhấn Đăng nhập."""
        # FIX: Chờ form sẵn sàng trước khi điền
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD))

        if username:
            self.send_keys_to_element(self.USERNAME_FIELD, username)
        if password:
            self.send_keys_to_element(self.PASSWORD_FIELD, password)

        self.click_element(self.LOGIN_BUTTON)
        # FIX: Bỏ time.sleep(1) cố định — conftest đã có wait_for_login_redirect

    def load_and_login(self, username, password):
        self.load()
        self.login(username, password)

    def get_error_message(self):
        try:
            element = WebDriverWait(self.driver, 7).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return element.text
        except TimeoutException:
            return None

    def is_login_successful(self):
        try:
            # FIX: Tăng timeout lên 15 giây khớp với DEFAULT_TIMEOUT
            WebDriverWait(self.driver, 15).until(
                lambda d: "/login" not in d.current_url
            )
            return True
        except TimeoutException:
            return False

    def click_signup_link(self):
        self.click_element(self.SIGNUP_LINK)

    def click_forgot_password_link(self):
        self.click_element(self.FORGOT_PASSWORD_LINK)

    def is_on_signup_page(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "/signup" in d.current_url.lower()
                or "/register" in d.current_url.lower()
            )
            return True
        except TimeoutException:
            return False

    def is_on_forgot_password_page(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "forgot" in d.current_url.lower()
                or "reset" in d.current_url.lower()
            )
            return True
        except TimeoutException:
            return False