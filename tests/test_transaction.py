import pytest
import time
from pages.transaction_page import TransactionPage
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from utils.excel_helper import ExcelHelper

class TestTransactionManagement:

    is_logged_in = False

    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.transaction_page = TransactionPage(driver, base_url)
        
        if not TestTransactionManagement.is_logged_in:
            driver.get(f"{base_url}/login")
            time.sleep(1) 
            login_page = LoginPage(driver, base_url)
            login_page.login("admin", "123456") 
            try:
                WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)
                TestTransactionManagement.is_logged_in = True
            except:
                pytest.fail("LỖI MẠNG: Web quay quá 10s không đăng nhập được.")

        driver.get(f"{base_url.rstrip('/')}/transactions") 
        driver.refresh() 
        time.sleep(1.5)

    def check_data_exists(self):
        """Hàm tiện ích: Kiểm tra có giao dịch nào để test không"""
        if self.transaction_page.get_transaction_count() == 0:
            pytest.skip("BỎ QUA: Không có dữ liệu giao dịch nào để test.")

    test_cases = ExcelHelper.get_data_from_testcase("Test_case_DATN.xlsx", "Quản lý mượn, trả")

    @pytest.mark.parametrize("tc", test_cases, ids=[tc["id"] for tc in test_cases])
    def test_transaction_from_excel(self, tc):
        tc_id = tc["id"]

        if tc_id == "TC_MT_001":
            self.check_data_exists() 
            self.transaction_page.click_remind_button()
            time.sleep(0.5) 
            assert self.transaction_page.is_remind_modal_open()

        elif tc_id == "TC_MT_002":
            self.check_data_exists()
            self.transaction_page.click_remind_button()
            time.sleep(0.5)
            self.transaction_page.send_reminder()
            time.sleep(1) 
            success_msg = self.transaction_page.get_success_message()
            if success_msg:
                assert "thành công" in success_msg.lower() or "gửi" in success_msg.lower()

        elif tc_id == "TC_MT_003":
            self.check_data_exists()
            self.transaction_page.click_remind_button()
            time.sleep(0.5)
            self.transaction_page.cancel_reminder()
            time.sleep(0.5)
            assert not self.transaction_page.is_remind_modal_open()

        elif tc_id == "TC_MT_004":
            self.check_data_exists()
            self.transaction_page.click_collect_button()
            time.sleep(0.5)
            assert self.transaction_page.is_collect_modal_open()

        elif tc_id == "TC_MT_005":
            self.check_data_exists()
            self.transaction_page.click_collect_button()
            time.sleep(0.5)
            self.transaction_page.confirm_collect_book()
            time.sleep(1.5)
            success_msg = self.transaction_page.get_success_message()
            if success_msg:
                assert "thu" in success_msg.lower() or "thành công" in success_msg.lower()

        elif tc_id == "TC_MT_006":
            self.check_data_exists()
            self.transaction_page.click_collect_button()
            time.sleep(0.5)
            self.transaction_page.cancel_collect()
            time.sleep(0.5)
            assert not self.transaction_page.is_collect_modal_open()

        elif tc_id == "TC_MT_007":
            self.check_data_exists()
            self.transaction_page.click_delete_button()
            time.sleep(0.5)
            assert self.transaction_page.is_delete_modal_open()

        elif tc_id == "TC_MT_008":
            self.check_data_exists()
            initial_count = self.transaction_page.get_transaction_count()
            self.transaction_page.click_delete_button()
            time.sleep(0.5)
            self.transaction_page.confirm_delete_transaction()
            time.sleep(1.5) 
            final_count = self.transaction_page.get_transaction_count()
            assert final_count < initial_count, "Số lượng giao dịch chưa bị giảm đi"

        elif tc_id == "TC_MT_009":
            self.check_data_exists()
            initial_count = self.transaction_page.get_transaction_count()
            self.transaction_page.click_delete_button()
            time.sleep(0.5)
            self.transaction_page.cancel_delete()
            time.sleep(0.5)
            assert not self.transaction_page.is_delete_modal_open()
            assert self.transaction_page.get_transaction_count() == initial_count

        else:
            pytest.skip(f"Test case {tc_id} chưa được định nghĩa logic xử lý.")