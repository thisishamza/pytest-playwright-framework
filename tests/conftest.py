import os
import pytest
import allure
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

pytest_plugins = [
    'fixtures.pages'
]

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    return context.new_page()

@pytest.fixture(scope="session")
def username():
    return os.getenv("USERNAME")

@pytest.fixture(scope="session")
def password():
    return os.getenv("PASSWORD")
