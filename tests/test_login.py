import pytest
from pages.login_page import LoginPage
from utils.excel_helper import ExcelHelper

class TestLogin:
   
    test_cases = ExcelHelper.get_data_from_testcase("Test_case_DATN.xlsx", "Đăng nhập")

    @pytest.mark.parametrize("tc", test_cases, ids=[tc["id"] for tc in test_cases])
    def test_login_from_excel(self, login_page, tc):
        tc_id = tc["id"]
        data = tc["data"]
        
        login_page.load()
        
        username = data.get("username", "")
        password = data.get("password", "")

        
        if tc_id in ["TC_DN_001", "TC_DN_002"]:
            login_page.login(username, password)
            assert login_page.is_login_successful(), f"[{tc_id}] Đăng nhập thất bại."

        elif tc_id in ["TC_DN_003", "TC_DN_004", "TC_DN_005"]:
            login_page.login(username, password)
            error_message = login_page.get_error_message()
            assert error_message is not None, f"[{tc_id}] Không hiện thông báo lỗi."
            assert "invalid" in error_message.lower() or "không hợp lệ" in error_message.lower() or "sai" in error_message.lower()

        elif tc_id == "TC_DN_006":
            login_page.send_keys_to_element(login_page.PASSWORD_FIELD, password)
            login_page.click_element(login_page.LOGIN_BUTTON)
            
            username_element = login_page.find_element(login_page.USERNAME_FIELD)
            validation_message = username_element.get_attribute("validationMessage")
            assert validation_message != "", "HTML5 validation message should appear"
            print(f"\n[Validation Message] Ô Tài khoản: '{validation_message}'")

        elif tc_id == "TC_DN_007":
            login_page.send_keys_to_element(login_page.USERNAME_FIELD, username)
            login_page.click_element(login_page.LOGIN_BUTTON)
            
            password_element = login_page.find_element(login_page.PASSWORD_FIELD)
            validation_message = password_element.get_attribute("validationMessage")
            assert validation_message != "", "HTML5 validation message should appear"
            print(f"\n[Validation Message] Ô Mật khẩu: '{validation_message}'") 

        elif tc_id == "TC_DN_008":
            login_page.click_element(login_page.LOGIN_BUTTON)
            
            username_element = login_page.find_element(login_page.USERNAME_FIELD)
            validation_message = username_element.get_attribute("validationMessage")
            assert validation_message != "", "HTML5 validation message should appear"
            print(f"\n[Validation Message] Ô Tài khoản: '{validation_message}'")

        elif tc_id == "TC_DN_009":
            login_page.click_signup_link()
            assert login_page.is_on_signup_page(), "Should navigate to signup page"

        elif tc_id == "TC_DN_010":
            login_page.click_forgot_password_link()
            assert login_page.is_on_forgot_password_page(), "Should navigate to forgot password page"
            
        else:
            pytest.skip(f"Test case {tc_id} chưa được định nghĩa logic xử lý.")