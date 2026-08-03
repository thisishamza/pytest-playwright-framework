"""
Shopping cart page object.
"""

from typing import List, Dict, Any
from playwright.sync_api import Page, Locator
from models.base_page import BasePage
from utils.logger import logger, log_step


class CartPage(BasePage):
    """Page object for the shopping cart page."""

    def __init__(self, page: Page):
        """Initialize cart page."""
        super().__init__(page, "/cart.html")

        # Page elements
        self.page_title = page.locator(".title")
        self.cart_list = page.locator(".cart_list")
        self.cart_items = page.locator(".cart_item")
        self.cart_item_labels = page.locator(".cart_item_label")

        # Cart quantity label
        self.cart_quantity_label = page.locator(".cart_quantity_label")
        self.cart_desc_label = page.locator(".cart_desc_label")

        # Buttons
        self.continue_shopping_button = page.locator("#continue-shopping")
        self.checkout_button = page.locator("#checkout")

    def get_cart_items_count(self) -> int:
        """
        Get the number of items in cart.

        Returns:
            Number of items in cart
        """
        return self.cart_items.count()

    def is_cart_empty(self) -> bool:
        """
        Check if cart is empty.

        Returns:
            True if cart is empty, False otherwise
        """
        return self.get_cart_items_count() == 0

    def get_cart_item_by_name(self, product_name: str) -> Locator:
        """
        Get cart item by product name.

        Args:
            product_name: Name of the product

        Returns:
            Locator for the cart item
        """
        return self.cart_items.filter(has_text=product_name)

    def get_cart_item_name(self, index: int) -> str:
        """
        Get cart item name by index.

        Args:
            index: Cart item index (0-based)

        Returns:
            Product name
        """
        item = self.cart_items.nth(index)
        name_element = item.locator(".inventory_item_name")
        return name_element.text_content() or ""

    def get_cart_item_description(self, index: int) -> str:
        """
        Get cart item description by index.

        Args:
            index: Cart item index (0-based)

        Returns:
            Product description
        """
        item = self.cart_items.nth(index)
        desc_element = item.locator(".inventory_item_desc")
        return desc_element.text_content() or ""

    def get_cart_item_price(self, index: int) -> float:
        """
        Get cart item price by index.

        Args:
            index: Cart item index (0-based)

        Returns:
            Product price as float
        """
        item = self.cart_items.nth(index)
        price_element = item.locator(".inventory_item_price")
        price_text = price_element.text_content() or "$0.00"
        # Remove dollar sign and convert to float
        return float(price_text.replace("$", ""))

    def get_cart_item_quantity(self, index: int) -> int:
        """
        Get cart item quantity by index.

        Args:
            index: Cart item index (0-based)

        Returns:
            Item quantity
        """
        item = self.cart_items.nth(index)
        qty_element = item.locator(".cart_quantity")
        qty_text = qty_element.text_content() or "1"
        return int(qty_text)

    def get_all_cart_items(self) -> List[Dict[str, Any]]:
        """
        Get all cart items with details.

        Returns:
            List of dictionaries containing item details
        """
        items = []
        count = self.get_cart_items_count()
        for i in range(count):
            items.append({
                "name": self.get_cart_item_name(i),
                "description": self.get_cart_item_description(i),
                "price": self.get_cart_item_price(i),
                "quantity": self.get_cart_item_quantity(i)
            })
        return items

    def get_all_cart_item_names(self) -> List[str]:
        """
        Get list of all product names in cart.

        Returns:
            List of product names
        """
        names = []
        count = self.get_cart_items_count()
        for i in range(count):
            names.append(self.get_cart_item_name(i))
        return names

    def remove_item_from_cart(self, product_name: str):
        """
        Remove an item from cart by product name.

        Args:
            product_name: Name of the product to remove
        """
        log_step(f"Removing item from cart: {product_name}")
        item = self.get_cart_item_by_name(product_name)
        remove_button = item.locator("button").filter(has_text="Remove")
        remove_button.click()

    def remove_item_from_cart_by_index(self, index: int):
        """
        Remove an item from cart by index.

        Args:
            index: Cart item index (0-based)
        """
        product_name = self.get_cart_item_name(index)
        log_step(f"Removing item at index {index} from cart: {product_name}")
        item = self.cart_items.nth(index)
        remove_button = item.locator("button").filter(has_text="Remove")
        remove_button.click()

    def remove_all_items_from_cart(self):
        """Remove all items from cart."""
        log_step("Removing all items from cart")
        while self.get_cart_items_count() > 0:
            self.remove_item_from_cart_by_index(0)
            # Small wait to ensure item is removed
            self.wait.wait_for_animation(100)

    def is_item_in_cart(self, product_name: str) -> bool:
        """
        Check if a specific item is in cart.

        Args:
            product_name: Name of the product

        Returns:
            True if item is in cart, False otherwise
        """
        item = self.get_cart_item_by_name(product_name)
        return item.is_visible()

    def click_item_name(self, product_name: str):
        """
        Click on item name to go to product details.

        Args:
            product_name: Name of the product
        """
        log_step(f"Clicking on cart item name: {product_name}")
        item = self.get_cart_item_by_name(product_name)
        name_link = item.locator(".inventory_item_name")
        name_link.click()

    def continue_shopping(self):
        """Click Continue Shopping button to go back to inventory."""
        log_step("Clicking Continue Shopping")
        self.continue_shopping_button.click()

    def proceed_to_checkout(self):
        """Click Checkout button to proceed to checkout."""
        log_step("Proceeding to checkout")
        self.checkout_button.click()

    def calculate_subtotal(self) -> float:
        """
        Calculate subtotal of all items in cart.

        Returns:
            Subtotal amount
        """
        items = self.get_all_cart_items()
        subtotal = 0
        for item in items:
            subtotal += item["price"] * item["quantity"]
        return round(subtotal, 2)

    def verify_cart_contains_items(self, expected_items: List[str]) -> bool:
        """
        Verify cart contains expected items.

        Args:
            expected_items: List of expected product names

        Returns:
            True if all expected items are in cart, False otherwise
        """
        actual_items = self.get_all_cart_item_names()
        for expected_item in expected_items:
            if expected_item not in actual_items:
                logger.error("Expected item '%s' not found in cart", expected_item)
                return False
        return True

    def verify_cart_has_exact_items(self, expected_items: List[str]) -> bool:
        """
        Verify cart has exactly the expected items (no more, no less).

        Args:
            expected_items: List of expected product names

        Returns:
            True if cart has exactly the expected items, False otherwise
        """
        actual_items = sorted(self.get_all_cart_item_names())
        expected_items = sorted(expected_items)

        if actual_items != expected_items:
            logger.error("Cart items mismatch. Expected: %s, Actual: %s",
                        expected_items, actual_items)
            return False
        return True

    def get_item_details(self, product_name: str) -> Dict[str, Any]:
        """
        Get details of a specific item in cart.

        Args:
            product_name: Name of the product

        Returns:
            Dictionary with item details

        Raises:
            ValueError: If item not found in cart
        """
        items = self.get_all_cart_items()
        for item in items:
            if item["name"] == product_name:
                return item
        raise ValueError(f"Item '{product_name}' not found in cart")

    def wait_for_cart_update(self, timeout: int = 2000):
        """
        Wait for cart to update after adding/removing items.

        Args:
            timeout: Timeout in milliseconds
        """
        self.wait.wait_for_animation(timeout)
