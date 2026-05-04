import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select  # Thêm thư viện xử lý menu Dropdown
from .base_page import BasePage

class BookPage(BasePage):

    def __init__(self, driver, base_url=None):
        super().__init__(driver)
        self.base_url = base_url

    ADD_BUTTON = (By.XPATH, "//button[contains(@onclick, 'openAddModal')]") # Tìm đích danh nút mở Modal
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Tìm tên sách')]")
    
    TITLE_INPUT = (By.ID, "bTitle")
    AUTHOR_INPUT = (By.ID, "bAuthor")
    CATEGORY_SELECT = (By.ID, "bCategory")
    QTY_INPUT = (By.ID, "bQty")
    AGE_INPUT = (By.ID, "bAge")
    DESC_INPUT = (By.ID, "bDesc")
    FUNFACT_INPUT = (By.ID, "bFunFact")
    SUBMIT_BTN = (By.ID, "modalSubmitBtn")
    
    CANCEL_BUTTON = (By.XPATH, "//button[@data-bs-dismiss='modal' and contains(., 'Hủy')]")

    CONFIRM_DELETE_BTN = (By.XPATH, "//button[contains(., 'Xóa ngay')]")
    CANCEL_DELETE_BTN = (By.XPATH, "//button[contains(., 'Hủy bỏ')]")

    def click_add_book_button(self):
        element = self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON))
        self.driver.execute_script("arguments[0].click();", element)
        self.wait.until(EC.visibility_of_element_located(self.TITLE_INPUT))

    def is_form_open(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.TITLE_INPUT))
            return True
        except:
            return False

    def fill_book_form(self, data):
        if 'title' in data:
            e = self.find_element(self.TITLE_INPUT)
            e.clear()
            e.send_keys(data['title'])
        if 'author' in data:
            e = self.find_element(self.AUTHOR_INPUT)
            e.clear()
            e.send_keys(data['author'])
        if 'category' in data:
            select = Select(self.find_element(self.CATEGORY_SELECT))
            select.select_by_visible_text(data['category'])
        if 'quantity' in data:
            e = self.find_element(self.QTY_INPUT)
            e.clear()
            e.send_keys(str(data['quantity']))
        if 'age' in data:
            e = self.find_element(self.AGE_INPUT)
            e.clear()
            e.send_keys(str(data['age']))
        if 'summary' in data:
            e = self.find_element(self.DESC_INPUT)
            e.clear()
            e.send_keys(data['summary'])
        if 'fun_fact' in data:
            e = self.find_element(self.FUNFACT_INPUT)
            e.clear()
            e.send_keys(data['fun_fact'])

    def submit_book_form(self):
        btn = self.find_element(self.SUBMIT_BTN)
        self.driver.execute_script("arguments[0].click();", btn)

    def cancel_form(self):
        btn = self.find_element(self.CANCEL_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)

    def book_exists_in_table(self, book_title):
        try:
            time.sleep(1) 
            tbody = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
            return book_title in tbody.text
        except:
            return False

    def click_edit_book(self, index=0):
        edit_buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'edit') or .//i[contains(@class, 'edit')]]")))
        if edit_buttons:
            self.driver.execute_script("arguments[0].click();", edit_buttons[index])

    def click_delete_book(self, index=0):
        delete_buttons = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'delete') or .//i[contains(@class, 'trash')]]")))
        if delete_buttons:
            self.driver.execute_script("arguments[0].click();", delete_buttons[index])

    def is_delete_modal_open(self):
        """Kiểm tra popup xóa bằng cách tìm nút 'Xóa ngay'"""
        try:
            return self.wait.until(EC.visibility_of_element_located(self.CONFIRM_DELETE_BTN)).is_displayed()
        except:
            return False

    def confirm_delete(self):
        """Bấm nút Xóa ngay"""
        btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_DELETE_BTN))
        self.driver.execute_script("arguments[0].click();", btn)

    def cancel_delete(self):
        """Bấm nút Hủy bỏ riêng của popup Xóa"""
        btn = self.wait.until(EC.element_to_be_clickable(self.CANCEL_DELETE_BTN))
        self.driver.execute_script("arguments[0].click();", btn)

    def search_book(self, text):
        search_input = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(text)
        search_input.send_keys(Keys.ENTER)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", search_input)
        time.sleep(1.5)

    def get_books_from_table(self):
        """Sửa lại: Chỉ đếm những dòng sách CÓ HIỂN THỊ trên màn hình"""
        try:
            rows = self.find_elements((By.XPATH, "//table/tbody/tr"))
            visible_rows = [row for row in rows if row.is_displayed()]
            
            if len(visible_rows) == 0:
                return 0
                
            first_text = visible_rows[0].text.lower()
            if len(visible_rows) == 1 and ("không" in first_text or "trống" in first_text or "no data" in first_text):
                return 0
                
            return len(visible_rows)
        except:
            return 0
    
    def add_book(self, data):
        self.click_add_book_button()
        self.fill_book_form(data)
        self.submit_book_form()
        time.sleep(1)