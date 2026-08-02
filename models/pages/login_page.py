from playwright.sync_api import Page, Locator

from models.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, url: str = ''):
        super().__init__(page, url)
        self.login_logo = page.locator('[class="login_logo"]')
        self.username = page.locator('#user-name')
        self.password = page.locator('#password')
        self.login_button = page.locator('#login-button')