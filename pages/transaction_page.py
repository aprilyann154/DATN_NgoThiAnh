from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class TransactionPage(BasePage):

    BTN_REMIND = (By.XPATH, "(//a[contains(@class, 'btn-remind')])[1]")
    BTN_COLLECT = (By.XPATH, "(//a[contains(@class, 'btn-return')])[1]")
    BTN_DELETE = (By.XPATH, "(//button[contains(@class, 'btn-delete')])[1]")

    SWAL_MODAL = (By.CLASS_NAME, "swal2-popup")
    SWAL_SHOW = (By.CSS_SELECTOR, ".swal2-popup.swal2-show")

    SWAL_CONFIRM_REMIND = (By.XPATH, "//button[contains(@class, 'swal2-confirm') and contains(text(), 'Gửi ngay')]")
    SWAL_CONFIRM_COLLECT = (By.XPATH, "//button[contains(@class, 'swal2-confirm') and contains(text(), 'Xác nhận')]")
    SWAL_CONFIRM_DELETE = (By.XPATH, "//button[contains(@class, 'swal2-confirm') and contains(text(), 'Đồng ý')]")

    SWAL_CANCEL_REMIND = (By.XPATH, "//button[contains(@class, 'swal2-cancel') and contains(text(), 'Hủy')]")
    SWAL_CANCEL_COLLECT = (By.XPATH, "//button[contains(@class, 'swal2-cancel') and contains(text(), 'Chưa')]")
    SWAL_CANCEL_DELETE = (By.XPATH, "//button[contains(@class, 'swal2-cancel') and contains(text(), 'Hủy')]")

    SUCCESS_MESSAGE = (By.ID, "swal2-title")
    HTML_CONTAINER = (By.ID, "swal2-html-container")

    TABLE_ROWS = (By.XPATH, "//table//tbody//tr")

    def __init__(self, driver, base_url: str = "http://localhost:3000"):
        super().__init__(driver)
        self.url = f"{base_url.rstrip('/')}/transactions"
        self.swal_wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get(self.url)

    def _wait_swal_open(self):
        self.swal_wait.until(
            EC.presence_of_element_located(self.SWAL_SHOW)
        )
        time.sleep(0.3)

    def _wait_swal_closed(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.SWAL_MODAL)
            )
        except Exception:
            pass

    def click_remind_button(self):
        self.click_element(self.BTN_REMIND)

    def is_remind_modal_open(self):
        try:
            self.swal_wait.until(
                EC.presence_of_element_located(self.SWAL_SHOW)
            )
            return True
        except TimeoutException:
            return False

    def send_reminder(self):
        self._wait_swal_open()
        self.click_element(self.SWAL_CONFIRM_REMIND)
        self._wait_swal_closed()

    def cancel_reminder(self):
        self._wait_swal_open()
        self.click_element(self.SWAL_CANCEL_REMIND)
        self._wait_swal_closed()

    def is_remind_button_disabled(self):
        try:
            btn = self.find_element(self.BTN_REMIND)
            return "disabled" in btn.get_attribute("class")
        except TimeoutException:
            return False

    def click_collect_button(self):
        self.click_element(self.BTN_COLLECT)

    def is_collect_modal_open(self):
        try:
            self.swal_wait.until(
                EC.presence_of_element_located(self.SWAL_SHOW)
            )
            return True
        except TimeoutException:
            return False

    def confirm_collect_book(self):
        self._wait_swal_open()
        self.click_element(self.SWAL_CONFIRM_COLLECT)
        self._wait_swal_closed()

    def cancel_collect(self):
        self._wait_swal_open()
        self.click_element(self.SWAL_CANCEL_COLLECT)
        self._wait_swal_closed()

    def click_delete_button(self):
        self.click_element(self.BTN_DELETE)

    def is_delete_modal_open(self):
        try:
            self.swal_wait.until(
                EC.presence_of_element_located(self.SWAL_SHOW)
            )
            return True
        except TimeoutException:
            return False

    def confirm_delete_transaction(self):
        self._wait_swal_open()
        self.click_element(self.SWAL_CONFIRM_DELETE)
        self._wait_swal_closed()

    def cancel_delete(self):
        self._wait_swal_open()
        self.click_element(self.SWAL_CANCEL_DELETE)
        self._wait_swal_closed()

    def get_success_message(self):
        try:
            title = self.find_element(self.SUCCESS_MESSAGE).text
            try:
                content = self.find_element(self.HTML_CONTAINER).text
                return f"{title} {content}"
            except Exception:
                return title
        except TimeoutException:
            return None

    def get_transaction_count(self):
        try:
            rows = self.find_elements(self.TABLE_ROWS)
            return len(rows) if rows else 0
        except TimeoutException:
            return 0