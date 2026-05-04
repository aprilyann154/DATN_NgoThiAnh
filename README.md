# Library Test Automation Project

Dự án kiểm thử tự động cho website thư viện sử dụng Selenium WebDriver với Python và pytest. Dự án được thiết kế theo mô hình POM (Page Object Model) chuyên nghiệp.

## Cấu trúc dự án

```text
libpro_test_automation/
├── pages/
│   ├── __init__.py                # Khởi tạo package pages
│   ├── base_page.py               # Chứa các hàm Selenium core (click, send_keys, wait...)
│   ├── login_page.py              # Page Object màn hình Đăng nhập
│   ├── book_page.py               # Page Object màn hình Quản lý sách
│   ├── borrow_page.py             # Page Object màn hình Đăng ký mượn sách
│   └── transaction_page.py        # Page Object màn hình Quản lý giao dịch (Mượn/Trả)
├── tests/
│   ├── conftest.py                # Cấu hình pytest, fixture WebDriver và Đăng nhập
│   ├── test_login.py              # Test case Đăng nhập (TC_DN)
│   ├── test_book_management.py    # Test case Quản lý sách (TC_QLS)
│   ├── test_borrow_books.py       # Test case Đăng ký mượn sách (TC_MS)
│   └── test_transaction.py        # Test case Quản lý giao dịch mượn/trả (TC_MT)
├── excel_test_runner.py           # Tool chạy test case trực tiếp từ file Excel 
├── requirements.txt               # Dependencies
└── README.md                      # Tài liệu dự án

# Cài đặt



1. Cài đặt Python 3.8+

2. Cài đặt dependencies:

   ```

   pip install -r requirements.txt

   ```


## Chạy test
### Chạy tất cả test:

```
python -m pytest tests/

```
### Chạy test cụ thể:

```
python -m pytest tests/test_login.py -v
python -m pytest tests/test_book_management.py -v
python -m pytest tests/test_transaction.py -v
python -m pytest tests/test_borrow_books.py -v

```

### Chạy xuất ra file xml:

```
python -m pytest tests/ -v --junitxml=result.xml

```
## Chạy xuất kết quả ra excel:
```
python excel_test_runner.py

```

## Cấu hình
conftest.py: Cung cấp fixture WebDriver (Microsoft Edge) và tự động thiết lập trạng thái đăng nhập cho các test case.

Test sử dụng BASE_URL (mặc định http://localhost:3000).

Tích hợp sẵn cơ chế kiểm tra và xử lý lỗi HTML5 Validation (chặn bỏ trống form của trình duyệt).