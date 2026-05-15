import os
import socket
import time
import urllib.parse

import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
LOGIN_PATH = os.getenv("LOGIN_PATH", "/login")
SKIP_SERVER_CHECK = os.getenv("SKIP_SERVER_CHECK", "false").lower() in {"1", "true", "yes"}
EDGE_BINARY_PATH = os.getenv(
    "EDGE_BINARY_PATH",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
)

ADMIN_CREDENTIALS = {
    "username": os.getenv("ADMIN_USERNAME", "admin"),
    "password": os.getenv("ADMIN_PASSWORD", "123456"),
}
USER_CREDENTIALS = {
    "username": os.getenv("USER_USERNAME", "anngo"),
    "password": os.getenv("USER_PASSWORD", "123456"),
}

DEFAULT_WAIT   = 15
PAGE_LOAD_WAIT = 30


def ensure_server_available(url: str, timeout: int = 10) -> None:
    if SKIP_SERVER_CHECK:
        return
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=5):
                return
        except OSError:
            time.sleep(0.5)
    raise RuntimeError(
        f"Server không hoạt động tại {url}. Hãy bật website trước khi chạy test!"
    )


def wait_for_login_redirect(driver, timeout: int = PAGE_LOAD_WAIT) -> None:
    """Chờ redirect khỏi /login xong."""
    WebDriverWait(driver, timeout).until(
        lambda d: "/login" not in d.current_url
    )
    time.sleep(1)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def driver():
    driver_path = os.path.join(os.getcwd(), "utils", "msedgedriver.exe")

    edge_options = Options()
    edge_options.add_argument("--ignore-certificate-errors")
    edge_options.add_argument("--allow-insecure-localhost")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    # SPA (React/Vue) dùng "eager" thay vì "normal"
    edge_options.page_load_strategy = "eager"
    edge_options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"]
    )
    edge_options.add_experimental_option("useAutomationExtension", False)

    if EDGE_BINARY_PATH and os.path.exists(EDGE_BINARY_PATH):
        edge_options.binary_location = EDGE_BINARY_PATH

    try:
        if os.path.exists(driver_path):
            service = Service(executable_path=driver_path)
            driver_instance = webdriver.Edge(service=service, options=edge_options)
        else:
            driver_instance = webdriver.Edge(options=edge_options)
    except Exception as e:
        raise RuntimeError(f"Không thể khởi động trình duyệt: {str(e)}")

    driver_instance.maximize_window()
    driver_instance.implicitly_wait(5)
    driver_instance.set_page_load_timeout(30)

    try:
        ensure_server_available(BASE_URL)
        driver_instance.get(BASE_URL)
        time.sleep(2)
    except Exception:
        pass

    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="session")
def login_page(driver, base_url):
    return LoginPage(driver, base_url)


@pytest.fixture
def admin_login(driver, login_page):
    ensure_server_available(BASE_URL)
    try:
        driver.delete_all_cookies()
        driver.execute_script(
            "window.localStorage.clear(); window.sessionStorage.clear();"
        )
    except Exception:
        pass

    login_page.load()
    login_page.login(ADMIN_CREDENTIALS["username"], ADMIN_CREDENTIALS["password"])
    wait_for_login_redirect(driver)
    return login_page


@pytest.fixture
def user_login(driver, login_page):
    ensure_server_available(BASE_URL)
    try:
        driver.delete_all_cookies()
        driver.execute_script(
            "window.localStorage.clear(); window.sessionStorage.clear();"
        )
    except Exception:
        pass

    login_page.load()
    login_page.login(USER_CREDENTIALS["username"], USER_CREDENTIALS["password"])
    wait_for_login_redirect(driver)
    return login_page