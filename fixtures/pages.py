import pytest
from playwright.sync_api import Page
import allure

from models.pages.home_page import HomePage
from models.pages.login_page import LoginPage


@allure.title("Login Page")
@pytest.fixture()
def login_page(page: Page, base_url: str):
    return LoginPage(page, base_url)


@allure.title("Home Page")
@pytest.fixture()
def home_page(page: Page, base_url: str):
    return HomePage(page, base_url)
