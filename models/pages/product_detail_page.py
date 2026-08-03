"""
Product detail page object for individual product view.
"""

from playwright.sync_api import Page
from models.base_page import BasePage
from utils.logger import logger, log_step


class ProductDetailPage(BasePage):
    """Page object for the product detail page."""

    def __init__(self, page: Page):
        """Initialize product detail page."""
        super().__init__(page, "/inventory-item.html")

        # Back button
        self.back_to_products_button = page.locator("#back-to-products")

        # Product details
        self.product_image = page.locator(".inventory_details_img")
        self.product_name = page.locator(".inventory_details_name")
        self.product_description = page.locator(".inventory_details_desc")
        self.product_price = page.locator(".inventory_details_price")

        # Add/Remove button
        self.add_to_cart_button = page.locator("button").filter(has_text="Add to cart")
        self.remove_button = page.locator("button").filter(has_text="Remove")

        # Cart
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def get_product_name(self) -> str:
        """
        Get the product name.

        Returns:
            Product name
        """
        return self.product_name.text_content() or ""

    def get_product_description(self) -> str:
        """
        Get the product description.

        Returns:
            Product description
        """
        return self.product_description.text_content() or ""

    def get_product_price(self) -> float:
        """
        Get the product price.

        Returns:
            Product price as float
        """
        price_text = self.product_price.text_content() or "$0.00"
        # Remove dollar sign and convert to float
        return float(price_text.replace("$", ""))

    def is_product_image_visible(self) -> bool:
        """
        Check if product image is visible.

        Returns:
            True if image is visible, False otherwise
        """
        return self.product_image.is_visible()

    def get_product_image_src(self) -> str:
        """
        Get the product image source URL.

        Returns:
            Image source URL
        """
        return self.product_image.get_attribute("src") or ""

    def add_to_cart(self):
        """Add the product to cart."""
        log_step(f"Adding product to cart: {self.get_product_name()}")
        self.add_to_cart_button.click()

    def remove_from_cart(self):
        """Remove the product from cart."""
        log_step(f"Removing product from cart: {self.get_product_name()}")
        self.remove_button.click()

    def is_added_to_cart(self) -> bool:
        """
        Check if product is added to cart.

        Returns:
            True if product is in cart, False otherwise
        """
        return self.remove_button.is_visible()

    def go_back_to_products(self):
        """Navigate back to products page."""
        log_step("Going back to products page")
        self.back_to_products_button.click()

    def go_to_cart(self):
        """Navigate to shopping cart."""
        log_step("Navigating to shopping cart")
        self.shopping_cart_link.click()

    def get_cart_count(self) -> int:
        """
        Get the number shown in cart badge.

        Returns:
            Cart item count, 0 if badge not visible
        """
        if self.cart_badge.is_visible():
            count_text = self.cart_badge.text_content() or "0"
            return int(count_text)
        return 0

    def verify_product_details(self, expected_name: str, expected_price: float) -> bool:
        """
        Verify product details match expected values.

        Args:
            expected_name: Expected product name
            expected_price: Expected product price

        Returns:
            True if details match, False otherwise
        """
        actual_name = self.get_product_name()
        actual_price = self.get_product_price()

        if actual_name != expected_name:
            logger.error("Product name mismatch. Expected: %s, Actual: %s",
                        expected_name, actual_name)
            return False

        if actual_price != expected_price:
            logger.error("Product price mismatch. Expected: %s, Actual: %s",
                        expected_price, actual_price)
            return False

        return True

    def wait_for_page_load(self):
        """Wait for product detail page to load."""
        self.wait.wait_for_element(".inventory_details_name")
        self.wait.wait_for_element(".inventory_details_img")
