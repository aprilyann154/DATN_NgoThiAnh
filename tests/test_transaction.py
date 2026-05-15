import pytest
import time
from pages.transaction_page import TransactionPage
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from utils.excel_helper import ExcelHelper

class TestTransactionManagement:

    @pytest.fixture(scope="class", autouse=True)
    def login_setup(self, driver, base_url):
        driver.get(f"{base_url.rstrip('/')}/login")
        login_page = LoginPage(driver, base_url)
        login_page.login("admin", "123456")
        WebDriverWait(driver, 10).until(lambda d: "/login" not in d.current_url)
        driver.get(f"{base_url.rstrip('/')}/transactions")

    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.transaction_page = TransactionPage(driver, base_url)
        if "/transactions" not in driver.current_url:
            driver.get(f"{base_url.rstrip('/')}/transactions")

    def check_data_exists(self):
        if self.transaction_page.get_transaction_count() == 0:
            pytest.skip("BỎ QUA: Không có dữ liệu giao dịch để test.")

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
            self.transaction_page.send_reminder()
            success_msg = self.transaction_page.get_success_message()
            if success_msg:
                assert any(word in success_msg.lower() for word in ["thành công", "gửi"])

        elif tc_id == "TC_MT_003":
            self.check_data_exists()
            self.transaction_page.click_remind_button()
            self.transaction_page.cancel_reminder()
            assert not self.transaction_page.is_remind_modal_open()

        elif tc_id == "TC_MT_004":
            self.check_data_exists()
            self.transaction_page.click_collect_button()
            time.sleep(0.5)
            assert self.transaction_page.is_collect_modal_open()

        elif tc_id == "TC_MT_005":
            self.check_data_exists()
            self.transaction_page.click_collect_button()
            self.transaction_page.confirm_collect_book()
            success_msg = self.transaction_page.get_success_message()
            if success_msg:
                assert any(word in success_msg.lower() for word in ["thu", "thành công"])

        elif tc_id == "TC_MT_006":
            self.check_data_exists()
            self.transaction_page.click_collect_button()
            self.transaction_page.cancel_collect()
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
            self.transaction_page.confirm_delete_transaction()
            final_count = self.transaction_page.get_transaction_count()
            assert final_count < initial_count

        elif tc_id == "TC_MT_009":
            self.check_data_exists()
            initial_count = self.transaction_page.get_transaction_count()
            self.transaction_page.click_delete_button()
            self.transaction_page.cancel_delete()
            assert not self.transaction_page.is_delete_modal_open()
            assert self.transaction_page.get_transaction_count() == initial_count

        else:
            pytest.skip(f"Test case {tc_id} chưa được định nghĩa.")