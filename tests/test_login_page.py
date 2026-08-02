import pytest
import allure
from playwright.sync_api import expect

from models.pages.home_page import HomePage
from models.pages.login_page import LoginPage


class TestLoginPage:

    @allure.title("Login Page UI Test")
    def test_login_page_ui(self, login_page: LoginPage):
        login_page.open()
        expect(login_page.login_logo).to_be_visible()
        expect(login_page.username).to_be_visible()
        expect(login_page.password).to_be_visible()
        expect(login_page.login_button).to_be_visible()

    @allure.title("Login Flow test")
    def test_login_flow(self, login_page: LoginPage, home_page: HomePage, username: str, password: str):
        login_page.open()
        login_page.username.fill(username)
        login_page.password.fill(password)
        login_page.login_button.click()
        # expect(login_page.page).to_have_url(home_page.url)
        expect(home_page.inventory_list).to_be_visible()

