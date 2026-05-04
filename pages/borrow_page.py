from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from .base_page import BasePage
import time

class BorrowPage(BasePage):
 
    REGISTER_BORROW_BUTTON = (By.XPATH, "//button[contains(@onclick, 'openConfigModalFromCard') or contains(text(), 'Đăng ký mượn')]")

    BORROW_DATE_FIELD = (By.XPATH, "(//input[@placeholder='DD/MM/YYYY'])[1]")
    RETURN_DATE_FIELD = (By.XPATH, "(//input[@placeholder='DD/MM/YYYY'])[2]")
    
    QUANTITY_INPUT = (By.ID, "cQty")
    BORROW_NOW_BUTTON = (By.XPATH, "//button[contains(@onclick, 'proceedToConfirm')]")
    
    CONFIRM_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and contains(@class, 'form-check-input')]")
    CONFIRM_BORROW_BUTTON = (By.XPATH, "//button[@type='submit' and contains(text(), 'Xác nhận')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(@data-bs-toggle, 'modal') and contains(text(), 'Quay lại')]")

    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(),'thành công') or contains(@class, 'swal2-success')]")
    RETURN_BUTTON = (By.XPATH, "//tr[1]//button[contains(@class, 'return')]")
    CONFIRM_RETURN_BUTTON = (By.ID, "confirm-return")
    RETURN_SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(),'thành công')]")
    OVERDUE_TABLE_ROW = (By.XPATH, "//table[@id='overdue-books-table']//tr")

    def __init__(self, driver, base_url: str = "http://localhost:3000"):
        super().__init__(driver)
        self.base_url = base_url.rstrip('/')
        self.url = f"{self.base_url}/books" 

    def load(self):
        """Load trang danh sách sách."""
        self.driver.get(self.url)

    def click_register_borrow(self, index=0):
        """Tìm và click vào nút 'Đăng ký mượn' bằng JavaScript để chống lỗi bị che khuất"""
        buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., 'Đăng ký mượn')]")))
        
        if buttons and len(buttons) > index:
            self.driver.execute_script("arguments[0].click();", buttons[index])
        else:
            raise Exception(f"Không tìm thấy nút 'Đăng ký mượn' ở vị trí {index}")

    def set_borrow_dates(self, borrow_date, return_date):
        """Điền ngày mượn và ngày trả."""
        self.clear_and_send_keys(self.BORROW_DATE_FIELD, borrow_date)
        self.clear_and_send_keys(self.RETURN_DATE_FIELD, return_date)

    def set_quantity(self, quantity):
        """Nhập số lượng mượn trực tiếp vào ô input."""
        self.clear_and_send_keys(self.QUANTITY_INPUT, str(quantity))

    def click_borrow_now(self):
        """Nhấn nút 'Mượn ngay' để chuyển sang bước kiểm tra nội quy."""
        self.click_element(self.BORROW_NOW_BUTTON)

    def confirm_rules_and_submit(self):
        """Tích chọn ô đồng ý nội quy và nhấn Xác nhận."""
        self.click_element(self.CONFIRM_CHECKBOX)
        self.click_element(self.CONFIRM_BORROW_BUTTON)
        
    def click_back_button(self):
        """Nhấn nút Quay lại trong popup xác nhận."""
        self.click_element(self.BACK_BUTTON)

    def borrow_book(self, borrow_date, return_date, quantity=1, book_index=0):
        """
        Flow thao tác tự động mượn sách hoàn chỉnh.
        Lưu ý: Không truyền tham số borrower_name vì giao diện không có ô chọn người mượn.
        """
        self.click_register_borrow(book_index)
        time.sleep(1) 
        
        self.set_borrow_dates(borrow_date, return_date)
        self.set_quantity(quantity)
        self.click_borrow_now()
        
        time.sleep(1) 
        self.confirm_rules_and_submit()

    def is_borrow_successful(self):
        """Kiểm tra có hiển thị thông báo mượn thành công hay không."""
        try:
            self.find_element(self.SUCCESS_MESSAGE)
            return True
        except TimeoutException:
            return False

    def return_book(self, borrowed_index=0):
        self.driver.get(f"{self.base_url}/borrowed-books")
        self.click_element(self.RETURN_BUTTON)
        self.click_element(self.CONFIRM_RETURN_BUTTON)

    def is_return_successful(self):
        try:
            self.find_element(self.RETURN_SUCCESS_MESSAGE)
            return True
        except TimeoutException:
            return False

    def open_overdue_books(self):
        self.driver.get(f"{self.base_url}/overdue-books")

    def get_overdue_book_count(self):
        rows = self.find_elements(self.OVERDUE_TABLE_ROW)
        return len(rows)