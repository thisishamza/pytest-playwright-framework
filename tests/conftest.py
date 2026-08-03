import os
import pytest
import allure
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pathlib import Path

load_dotenv()

from config.test_users import TestUsers
from data.test_data import TestData

pytest_plugins = [
    'fixtures.pages'
]


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://www.saucedemo.com")


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright, browser_name, request):
    headless = request.config.getoption("--headless", default=True)

    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=headless)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=headless)
    else:
        browser = playwright.chromium.launch(headless=headless)

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    page.set_default_timeout(30000)
    return page


@pytest.fixture(scope="session")
def username():
    return os.getenv("USERNAME", "standard_user")


@pytest.fixture(scope="session")
def password():
    return os.getenv("PASSWORD", "secret_sauce")


@pytest.fixture
def standard_user():
    return TestUsers.get_user("standard_user")


@pytest.fixture
def locked_out_user():
    return TestUsers.get_user("locked_out_user")


@pytest.fixture
def problem_user():
    return TestUsers.get_user("problem_user")


@pytest.fixture
def performance_glitch_user():
    return TestUsers.get_user("performance_glitch_user")


@pytest.fixture
def error_user():
    return TestUsers.get_user("error_user")


@pytest.fixture
def visual_user():
    return TestUsers.get_user("visual_user")


@pytest.fixture(params=TestUsers.get_all_usernames())
def all_users(request):
    return TestUsers.get_user(request.param)


@pytest.fixture(
    params=["standard_user", "problem_user", "performance_glitch_user", "error_user", "visual_user"]
)
def users_that_can_login(request):
    return TestUsers.get_user(request.param)


@pytest.fixture(params=["standard_user", "performance_glitch_user", "visual_user"])
def users_that_can_checkout(request):
    return TestUsers.get_user(request.param)


@pytest.fixture
def valid_checkout_data():
    return TestData.get_valid_checkout_data()[0]


@pytest.fixture
def invalid_checkout_data():
    return TestData.get_invalid_checkout_data()


@pytest.fixture
def product_data():
    return TestData.get_product_list()


@pytest.fixture
def expected_products():
    return TestData.get_sorted_products("az")


@pytest.fixture
def login_and_go_to_inventory(page, login_page, inventory_page, standard_user):
    login_page.open()
    login_page.login(standard_user["username"], standard_user["password"])
    inventory_page.wait.wait_for_element(".inventory_list")
    return inventory_page


@pytest.fixture
def add_items_to_cart(login_and_go_to_inventory):
    inventory_page = login_and_go_to_inventory
    for i in range(3):
        inventory_page.add_product_to_cart_by_index(i)
    return inventory_page


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        if "page" in item.fixturenames:
            page = item.funcargs["page"]

            screenshot_dir = Path("reports/screenshots/failures")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            screenshot_path = screenshot_dir / f"{item.nodeid.replace('::', '_')}.png"
            page.screenshot(path=str(screenshot_path))

            if allure:
                with open(screenshot_path, "rb") as image:
                    allure.attach(
                        image.read(),
                        name="failure_screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
