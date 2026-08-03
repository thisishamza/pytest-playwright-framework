import pytest
from playwright.sync_api import Page
import allure

from models.pages.login_page import LoginPage
from models.pages.inventory_page import InventoryPage
from models.pages.product_detail_page import ProductDetailPage
from models.pages.cart_page import CartPage
from models.pages.checkout_info_page import CheckoutInfoPage
from models.pages.checkout_overview_page import CheckoutOverviewPage
from models.pages.checkout_complete_page import CheckoutCompletePage
from models.components.header import HeaderComponent
from models.components.sidebar_menu import SidebarMenuComponent
from models.components.product_card import ProductCardFactory


@allure.title("Login Page")
@pytest.fixture()
def login_page(page: Page, base_url: str):
    return LoginPage(page, base_url)


@allure.title("Inventory Page")
@pytest.fixture()
def inventory_page(page: Page):
    return InventoryPage(page)


@allure.title("Product Detail Page")
@pytest.fixture()
def product_detail_page(page: Page):
    return ProductDetailPage(page)


@allure.title("Cart Page")
@pytest.fixture()
def cart_page(page: Page):
    return CartPage(page)


@allure.title("Checkout Info Page")
@pytest.fixture()
def checkout_info_page(page: Page):
    return CheckoutInfoPage(page)


@allure.title("Checkout Overview Page")
@pytest.fixture()
def checkout_overview_page(page: Page):
    return CheckoutOverviewPage(page)


@allure.title("Checkout Complete Page")
@pytest.fixture()
def checkout_complete_page(page: Page):
    return CheckoutCompletePage(page)


@allure.title("Header Component")
@pytest.fixture()
def header_component(page: Page):
    return HeaderComponent(page)


@allure.title("Sidebar Menu Component")
@pytest.fixture()
def sidebar_menu(page: Page):
    return SidebarMenuComponent(page)


@allure.title("Product Card Factory")
@pytest.fixture()
def product_card_factory(page: Page):
    return ProductCardFactory(page)
