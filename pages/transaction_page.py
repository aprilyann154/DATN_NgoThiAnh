from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
import time

class TransactionPage(BasePage):

    BTN_REMIND = (By.XPATH, "(//a[contains(@class, 'btn-remind')])[1]")
    BTN_COLLECT = (By.XPATH, "(//a[contains(@class, 'btn-return')])[1]")
    BTN_DELETE = (By.XPATH, "(//button[contains(@class, 'btn-delete')])[1]")

    SWAL_MODAL = (By.CLASS_NAME, "swal2-popup")

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

    def load(self):
        """Load the transaction management page."""
        self.driver.get(self.url)

    def click_remind_button(self):
        self.click_element(self.BTN_REMIND)

    def is_remind_modal_open(self):
        try:
            return self.find_element(self.SWAL_MODAL).is_displayed()
        except TimeoutException:
            return False

    def send_reminder(self):
        self.click_element(self.SWAL_CONFIRM_REMIND)
        time.sleep(1) 

    def cancel_reminder(self):
        self.click_element(self.SWAL_CANCEL_REMIND)
        time.sleep(0.5)

    def is_remind_button_disabled(self):
        """Kiểm tra xem nút nhắc nhở có bị disable sau khi gửi không"""
        try:
            btn = self.find_element(self.BTN_REMIND)
            classes = btn.get_attribute("class")
            return "disabled" in classes
        except TimeoutException:
            return False

    def click_collect_button(self):
        self.click_element(self.BTN_COLLECT)

    def is_collect_modal_open(self):
        try:
            return self.find_element(self.SWAL_MODAL).is_displayed()
        except TimeoutException:
            return False

    def confirm_collect_book(self):
        self.click_element(self.SWAL_CONFIRM_COLLECT)
        time.sleep(1)

    def cancel_collect(self):
        self.click_element(self.SWAL_CANCEL_COLLECT)
        time.sleep(0.5)

    def click_delete_button(self):
        self.click_element(self.BTN_DELETE)

    def is_delete_modal_open(self):
        try:
            return self.find_element(self.SWAL_MODAL).is_displayed()
        except TimeoutException:
            return False

    def confirm_delete_transaction(self):
        self.click_element(self.SWAL_CONFIRM_DELETE)
        time.sleep(1)

    def cancel_delete(self):
        self.click_element(self.SWAL_CANCEL_DELETE)
        time.sleep(0.5)

    def get_success_message(self):
        """Lấy text từ popup thông báo thành công của SweetAlert2"""
        try:
            title = self.find_element(self.SUCCESS_MESSAGE).text
            try:
                content = self.find_element(self.HTML_CONTAINER).text
                return f"{title} {content}"
            except:
                return title
        except TimeoutException:
            return None

    def get_transaction_count(self):
        """Đếm số lượng giao dịch hiện có trong bảng"""
        try:
            rows = self.find_elements(self.TABLE_ROWS)
            return len(rows) if rows else 0
        except TimeoutException:
            return 0