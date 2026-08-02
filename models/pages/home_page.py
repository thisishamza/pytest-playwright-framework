from playwright.sync_api import Page, Locator

from models.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page, url: str = '/inventory.html'):
        super().__init__(page, url)
        self.app_logo = page.locator('[class="app_logo"]')
        self.shopping_cart = page.locator('#shopping_cart_container')
        self.inventory_list = page.locator('.inventory_list')
