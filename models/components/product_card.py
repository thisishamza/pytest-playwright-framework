"""
Product card component for inventory page.
"""

from playwright.sync_api import Page, Locator
from utils.logger import log_step


class ProductCardComponent:
    """Reusable product card component."""

    def __init__(self, page: Page, product_locator: Locator):
        """
        Initialize product card component.

        Args:
            page: Playwright page instance
            product_locator: Locator for the specific product card
        """
        self.page = page
        self.product = product_locator

        # Product elements within the card
        self.image_link = product_locator.locator(".inventory_item_img a")
        self.image = product_locator.locator(".inventory_item_img img")
        self.name = product_locator.locator(".inventory_item_name")
        self.description = product_locator.locator(".inventory_item_desc")
        self.price_bar = product_locator.locator(".pricebar")
        self.price = product_locator.locator(".inventory_item_price")
        self.add_to_cart_button = product_locator.locator("button").filter(has_text="Add to cart")
        self.remove_button = product_locator.locator("button").filter(has_text="Remove")

    def get_name(self) -> str:
        """
        Get product name.

        Returns:
            Product name
        """
        return self.name.text_content() or ""

    def get_description(self) -> str:
        """
        Get product description.

        Returns:
            Product description
        """
        return self.description.text_content() or ""

    def get_price(self) -> float:
        """
        Get product price.

        Returns:
            Product price as float
        """
        price_text = self.price.text_content() or "$0.00"
        # Remove dollar sign and convert to float
        return float(price_text.replace("$", ""))

    def get_price_text(self) -> str:
        """
        Get product price as displayed text.

        Returns:
            Product price text with currency symbol
        """
        return self.price.text_content() or "$0.00"

    def get_image_src(self) -> str:
        """
        Get product image source URL.

        Returns:
            Image source URL
        """
        return self.image.get_attribute("src") or ""

    def get_image_alt(self) -> str:
        """
        Get product image alt text.

        Returns:
            Image alt text
        """
        return self.image.get_attribute("alt") or ""

    def is_in_cart(self) -> bool:
        """
        Check if product is in cart.

        Returns:
            True if product is in cart (Remove button visible), False otherwise
        """
        return self.remove_button.is_visible()

    def add_to_cart(self):
        """Add product to cart."""
        product_name = self.get_name()
        log_step(f"Adding product to cart: {product_name}")
        self.add_to_cart_button.click()

    def remove_from_cart(self):
        """Remove product from cart."""
        product_name = self.get_name()
        log_step(f"Removing product from cart: {product_name}")
        self.remove_button.click()

    def click_product_name(self):
        """Click product name to go to detail page."""
        product_name = self.get_name()
        log_step(f"Clicking product name: {product_name}")
        self.name.click()

    def click_product_image(self):
        """Click product image to go to detail page."""
        product_name = self.get_name()
        log_step(f"Clicking product image: {product_name}")
        self.image_link.click()

    def is_visible(self) -> bool:
        """
        Check if product card is visible.

        Returns:
            True if product card is visible, False otherwise
        """
        return self.product.is_visible()

    def get_button_text(self) -> str:
        """
        Get current button text (Add to cart or Remove).

        Returns:
            Button text
        """
        if self.add_to_cart_button.is_visible():
            return "Add to cart"
        if self.remove_button.is_visible():
            return "Remove"
        return ""

    def verify_product_details(
        self,
        expected_name: str = None,
        expected_price: float = None,
        expected_description: str = None
    ) -> bool:
        """
        Verify product details match expected values.

        Args:
            expected_name: Expected product name
            expected_price: Expected product price
            expected_description: Expected product description

        Returns:
            True if all provided details match, False otherwise
        """
        if expected_name and self.get_name() != expected_name:
            log_step(f"Name mismatch. Expected: {expected_name}, Actual: {self.get_name()}")
            return False

        if expected_price and abs(self.get_price() - expected_price) > 0.01:
            log_step(f"Price mismatch. Expected: ${expected_price}, Actual: ${self.get_price()}")
            return False

        if expected_description and self.get_description() != expected_description:
            log_step(f"Description mismatch. Expected: {expected_description}, Actual: {self.get_description()}")
            return False

        return True

    def get_all_details(self) -> dict:
        """
        Get all product card details.

        Returns:
            Dictionary with all product details
        """
        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "price": self.get_price(),
            "price_text": self.get_price_text(),
            "image_src": self.get_image_src(),
            "image_alt": self.get_image_alt(),
            "in_cart": self.is_in_cart(),
            "button_text": self.get_button_text()
        }


class ProductCardFactory:
    """Factory for creating ProductCard components."""

    def __init__(self, page: Page):
        """
        Initialize product card factory.

        Args:
            page: Playwright page instance
        """
        self.page = page

    def get_product_card_by_index(self, index: int) -> ProductCardComponent:
        """
        Get product card by index.

        Args:
            index: Product index (0-based)

        Returns:
            ProductCardComponent instance
        """
        product_locator = self.page.locator(".inventory_item").nth(index)
        return ProductCardComponent(self.page, product_locator)

    def get_product_card_by_name(self, product_name: str) -> ProductCardComponent:
        """
        Get product card by product name.

        Args:
            product_name: Name of the product

        Returns:
            ProductCardComponent instance
        """
        product_locator = self.page.locator(".inventory_item").filter(has_text=product_name)
        return ProductCardComponent(self.page, product_locator)

    def get_all_product_cards(self) -> list:
        """
        Get all product cards on the page.

        Returns:
            List of ProductCardComponent instances
        """
        cards = []
        product_count = self.page.locator(".inventory_item").count()
        for i in range(product_count):
            cards.append(self.get_product_card_by_index(i))
        return cards
