import pytest
import time
from pages.book_page import BookPage
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from utils.excel_helper import ExcelHelper

class TestBookManagement:

    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        """Setup đăng nhập thông minh và tự làm sạch màn hình trước mỗi case."""
        self.book_page = BookPage(driver, base_url)
        
        # Thêm điều kiện dự phòng f"{base_url.rstrip('/')}/" để bắt dính mọi trường hợp trang chủ
        if "login" in driver.current_url or driver.current_url in ["data:,", "about:blank"] or driver.current_url == f"{base_url.rstrip('/')}/":
            login_page = LoginPage(driver, base_url)
            login_page.load()
            login_page.login("admin", "123456") 
            try:
                WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)
            except:
                pass
            time.sleep(2) # <--- NHỊP NGHỈ 1: Chờ web lưu xong trạng thái đăng nhập

        driver.get(f"{base_url.rstrip('/')}/books")
        driver.refresh()
        time.sleep(1.5)

    test_cases_add = ExcelHelper.get_data_from_testcase("Test_case_DATN.xlsx", "Quản lý sách - Thêm mới sách")
    test_cases_edit = ExcelHelper.get_data_from_testcase("Test_case_DATN.xlsx", "Quản lý sách - Chỉnh sửa sách")
    test_cases_del_search = ExcelHelper.get_data_from_testcase("Test_case_DATN.xlsx", "Quản lý sách - Xóa, tìm kiếm ")

    @pytest.mark.parametrize("tc", test_cases_add, ids=[tc["id"] for tc in test_cases_add])
    def test_add_book_from_excel(self, tc):
        tc_id = tc["id"]
        data = tc["data"]
        
        if tc_id == "TC_QLS_001":
            time.sleep(2) 
            self.book_page.click_add_book_button()
            assert self.book_page.is_form_open(), "Form Thêm sách không hiển thị"

        elif tc_id in ["TC_QLS_002", "TC_QLS_003"]:
            title = data.get('Tên sách', 'Sách Mới') + f" {int(time.time())}"
            book_data = {
                'title': title,
                'author': data.get('Tác giả', ''),
                'category': data.get('Thể loại', ''),
                'quantity': data.get('Số lượng', ''),
                'summary': data.get('Nội dung tóm tắt', '')
            }
            self.book_page.click_add_book_button()
            time.sleep(0.5)
            self.book_page.fill_book_form(book_data)
            self.book_page.submit_book_form()
            
            time.sleep(1.5)
            assert self.book_page.book_exists_in_table(title), f"[{tc_id}] Sách không được thêm vào bảng!"

        elif tc_id == "TC_QLS_004":
            self.book_page.click_add_book_button()
            self.book_page.submit_book_form()
            title_element = self.book_page.find_element(self.book_page.TITLE_INPUT)
            assert title_element.get_attribute("validationMessage") != "", "HTML5 phải chặn khi để trống"

        elif tc_id == "TC_QLS_005":
            self.book_page.click_add_book_button()
            book_data = {'title': 'Test Lỗi Số', 'author': 'A', 'category': 'Văn học Việt Nam', 'quantity': data.get('Chữ cái', 'abc')}
            self.book_page.fill_book_form(book_data)
            self.book_page.submit_book_form()
            qty_element = self.book_page.find_element(self.book_page.QTY_INPUT)
            assert qty_element.get_attribute("validationMessage") != "", "HTML5 phải chặn nhập chữ vào ô số"

        elif tc_id == "TC_QLS_006":
            initial_count = self.book_page.get_books_from_table()
            self.book_page.click_add_book_button()
            self.book_page.cancel_form()
            time.sleep(1)
            assert not self.book_page.is_form_open()
            assert initial_count == self.book_page.get_books_from_table(), "Số lượng sách trong bảng bị thay đổi"

    @pytest.mark.parametrize("tc", test_cases_edit, ids=[tc["id"] for tc in test_cases_edit])
    def test_edit_book_from_excel(self, tc):
        tc_id = tc["id"]
        data = tc["data"]

        if tc_id == "TC_QLS_007":
            self.book_page.click_edit_book(0)
            assert self.book_page.is_form_open()

        elif tc_id == "TC_QLS_008":
            self.book_page.click_edit_book(0)
            fields = [self.book_page.TITLE_INPUT, self.book_page.AUTHOR_INPUT, self.book_page.QTY_INPUT]
            for field in fields:
                assert len(self.book_page.find_elements(field)) > 0

        elif tc_id == "TC_QLS_009":
            temp_title = f"Sách Sắp Sửa {int(time.time())}"
            self.book_page.add_book({'title': temp_title, 'author': 'A', 'category': 'Văn học Việt Nam', 'quantity': 1})
            time.sleep(1.5)
            self.book_page.click_edit_book(0)
            
            updated_title = data.get('Tên sách', 'Sách Đã Cập Nhật') + f" {int(time.time())}"
            self.book_page.fill_book_form({'title': updated_title})
            self.book_page.submit_book_form()
            time.sleep(1.5)
            assert self.book_page.book_exists_in_table(updated_title)

        elif tc_id == "TC_QLS_010":
            self.book_page.click_edit_book(0)
            title_field = self.book_page.find_element(self.book_page.TITLE_INPUT)
            title_field.clear()
            self.book_page.submit_book_form()
            assert title_field.get_attribute("validationMessage") != ""

        elif tc_id == "TC_QLS_011":
            self.book_page.click_edit_book(0)
            self.book_page.fill_book_form({'quantity': 'abc'})
            self.book_page.submit_book_form()
            qty_element = self.book_page.find_element(self.book_page.QTY_INPUT)
            assert qty_element.get_attribute("validationMessage") != ""

        elif tc_id == "TC_QLS_012":
            original_title = self.book_page.find_element((By.XPATH, "//table/tbody/tr[1]/td[2]")).text
            self.book_page.click_edit_book(0)
            title_field = self.book_page.find_element(self.book_page.TITLE_INPUT)
            title_field.clear()
            title_field.send_keys("Hủy sửa")
            self.book_page.cancel_form()
            time.sleep(1)
            assert self.book_page.book_exists_in_table(original_title)


    @pytest.mark.parametrize("tc", test_cases_del_search, ids=[tc["id"] for tc in test_cases_del_search])
    def test_del_search_from_excel(self, tc):
        tc_id = tc["id"]
        
        import openpyxl
        wb = openpyxl.load_workbook("Test_case_DATN.xlsx", data_only=True)
        sheet = wb["Quản lý sách - Xóa, tìm kiếm "]
        search_keyword = ""
        for row in sheet.iter_rows(min_row=10, values_only=True):
            if row[0] == tc_id:
                search_keyword = str(row[3] or "")
                break

        if tc_id == "TC_QLS_013":
            self.book_page.click_delete_book(0)
            assert self.book_page.is_delete_modal_open()
            self.book_page.cancel_delete()

        elif tc_id == "TC_QLS_014":
            temp_title = f"Sách Để Xóa {int(time.time())}"
            self.book_page.add_book({'title': temp_title, 'author': 'A', 'category': 'Văn học Việt Nam', 'quantity': 1})
            time.sleep(1.5)
            self.book_page.click_delete_book(0)
            self.book_page.confirm_delete()
            time.sleep(1.5)
            assert not self.book_page.book_exists_in_table(temp_title)

        elif tc_id == "TC_QLS_015":
            original_title = self.book_page.find_element((By.XPATH, "//table/tbody/tr[1]/td[2]")).text
            self.book_page.click_delete_book(0)
            time.sleep(1)
            self.book_page.cancel_delete()
            time.sleep(1)
            assert self.book_page.book_exists_in_table(original_title)
            assert not self.book_page.is_delete_modal_open()

        elif tc_id == "TC_QLS_016":
            self.book_page.search_book(search_keyword)
            time.sleep(1.5)
            assert self.book_page.get_books_from_table() > 0

        elif tc_id == "TC_QLS_017":
            self.book_page.search_book(search_keyword)
            time.sleep(1.5)
            assert self.book_page.get_books_from_table() == 0