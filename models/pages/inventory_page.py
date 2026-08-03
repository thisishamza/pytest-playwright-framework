"""
Inventory page object for product listing and management.
"""

from typing import List
from playwright.sync_api import Page, Locator
from models.base_page import BasePage
from utils.logger import logger, log_step


class InventoryPage(BasePage):
    """Page object for the inventory/products page."""

    def __init__(self, page: Page):
        """Initialize inventory page."""
        super().__init__(page, "/inventory.html")

        # Header elements
        self.app_logo = page.locator(".app_logo")
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.burger_menu_button = page.locator("#react-burger-menu-btn")

        # Page title and sorting
        self.page_title = page.locator(".title")
        self.sort_dropdown = page.locator(".product_sort_container")

        # Product grid
        self.inventory_container = page.locator("#inventory_container")
        self.inventory_list = page.locator(".inventory_list")
        self.inventory_items = page.locator(".inventory_item")

        # Footer
        self.footer = page.locator("footer")
        self.social_twitter = page.locator(".social_twitter")
        self.social_facebook = page.locator(".social_facebook")
        self.social_linkedin = page.locator(".social_linkedin")

    def get_product_count(self) -> int:
        """Get the number of products displayed."""
        return self.inventory_items.count()

    def get_product_by_name(self, product_name: str) -> Locator:
        """
        Get a product element by its name.

        Args:
            product_name: Name of the product

        Returns:
            Locator for the product container
        """
        return self.inventory_items.filter(has_text=product_name)

    def get_product_name(self, index: int) -> str:
        """
        Get product name by index.

        Args:
            index: Product index (0-based)

        Returns:
            Product name
        """
        product = self.inventory_items.nth(index)
        name_element = product.locator(".inventory_item_name")
        return name_element.text_content() or ""

    def get_product_description(self, index: int) -> str:
        """
        Get product description by index.

        Args:
            index: Product index (0-based)

        Returns:
            Product description
        """
        product = self.inventory_items.nth(index)
        desc_element = product.locator(".inventory_item_desc")
        return desc_element.text_content() or ""

    def get_product_price(self, index: int) -> float:
        """
        Get product price by index.

        Args:
            index: Product index (0-based)

        Returns:
            Product price as float
        """
        product = self.inventory_items.nth(index)
        price_element = product.locator(".inventory_item_price")
        price_text = price_element.text_content() or "$0.00"
        # Remove dollar sign and convert to float
        return float(price_text.replace("$", ""))

    def get_all_product_names(self) -> List[str]:
        """
        Get list of all product names.

        Returns:
            List of product names in display order
        """
        names = []
        count = self.get_product_count()
        for i in range(count):
            names.append(self.get_product_name(i))
        return names

    def get_all_product_prices(self) -> List[float]:
        """
        Get list of all product prices.

        Returns:
            List of product prices in display order
        """
        prices = []
        count = self.get_product_count()
        for i in range(count):
            prices.append(self.get_product_price(i))
        return prices

    def add_product_to_cart(self, product_name: str):
        """
        Add a product to cart by name.

        Args:
            product_name: Name of the product to add
        """
        log_step(f"Adding product to cart: {product_name}")
        product = self.get_product_by_name(product_name)
        add_button = product.locator("button").filter(has_text="Add to cart")
        add_button.click()

    def add_product_to_cart_by_index(self, index: int):
        """
        Add a product to cart by index.

        Args:
            index: Product index (0-based)
        """
        product_name = self.get_product_name(index)
        log_step(f"Adding product at index {index} to cart: {product_name}")
        product = self.inventory_items.nth(index)
        add_button = product.locator("button").filter(has_text="Add to cart")
        add_button.click()

    def remove_product_from_cart(self, product_name: str):
        """
        Remove a product from cart by name.

        Args:
            product_name: Name of the product to remove
        """
        log_step(f"Removing product from cart: {product_name}")
        product = self.get_product_by_name(product_name)
        remove_button = product.locator("button").filter(has_text="Remove")
        remove_button.click()

    def remove_product_from_cart_by_index(self, index: int):
        """
        Remove a product from cart by index.

        Args:
            index: Product index (0-based)
        """
        product_name = self.get_product_name(index)
        log_step(f"Removing product at index {index} from cart: {product_name}")
        product = self.inventory_items.nth(index)
        remove_button = product.locator("button").filter(has_text="Remove")
        remove_button.click()

    def is_product_added_to_cart(self, product_name: str) -> bool:
        """
        Check if a product is added to cart.

        Args:
            product_name: Name of the product

        Returns:
            True if product is in cart, False otherwise
        """
        product = self.get_product_by_name(product_name)
        remove_button = product.locator("button").filter(has_text="Remove")
        return remove_button.is_visible()

    def click_product_name(self, product_name: str):
        """
        Click on product name to go to product details.

        Args:
            product_name: Name of the product
        """
        log_step(f"Clicking on product name: {product_name}")
        product = self.get_product_by_name(product_name)
        name_link = product.locator(".inventory_item_name")
        name_link.click()

    def click_product_image(self, product_name: str):
        """
        Click on product image to go to product details.

        Args:
            product_name: Name of the product
        """
        log_step(f"Clicking on product image: {product_name}")
        product = self.get_product_by_name(product_name)
        image_link = product.locator(".inventory_item_img a")
        image_link.click()

    def sort_products(self, sort_option: str):
        """
        Sort products by specified option.

        Args:
            sort_option: Sort option value
                - "az" for Name (A to Z)
                - "za" for Name (Z to A)
                - "lohi" for Price (low to high)
                - "hilo" for Price (high to low)
        """
        log_step(f"Sorting products by: {sort_option}")
        self.sort_dropdown.select_option(value=sort_option)
        # Wait for sort to complete
        self.wait.wait_for_animation(500)

    def get_selected_sort_option(self) -> str:
        """
        Get currently selected sort option.

        Returns:
            Selected sort option value
        """
        return self.sort_dropdown.input_value()

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

    def go_to_cart(self):
        """Navigate to shopping cart."""
        log_step("Navigating to shopping cart")
        self.shopping_cart_link.click()

    def open_menu(self):
        """Open the burger menu."""
        log_step("Opening burger menu")
        self.burger_menu_button.click()
        # Wait for menu animation
        self.wait.wait_for_animation(300)

    def verify_products_sorted_alphabetically(self, ascending: bool = True) -> bool:
        """
        Verify products are sorted alphabetically.

        Args:
            ascending: True for A-Z, False for Z-A

        Returns:
            True if correctly sorted, False otherwise
        """
        names = self.get_all_product_names()
        sorted_names = sorted(names, reverse=not ascending)
        return names == sorted_names

    def verify_products_sorted_by_price(self, ascending: bool = True) -> bool:
        """
        Verify products are sorted by price.

        Args:
            ascending: True for low to high, False for high to low

        Returns:
            True if correctly sorted, False otherwise
        """
        prices = self.get_all_product_prices()
        sorted_prices = sorted(prices, reverse=not ascending)
        return prices == sorted_prices

    def get_products_in_cart(self) -> List[str]:
        """
        Get list of products that are in cart.

        Returns:
            List of product names in cart
        """
        products_in_cart = []
        count = self.get_product_count()
        for i in range(count):
            product = self.inventory_items.nth(i)
            remove_button = product.locator("button").filter(has_text="Remove")
            if remove_button.is_visible():
                products_in_cart.append(self.get_product_name(i))
        return products_in_cart

    def add_all_products_to_cart(self):
        """Add all products to cart."""
        log_step("Adding all products to cart")
        count = self.get_product_count()
        for i in range(count):
            product = self.inventory_items.nth(i)
            add_button = product.locator("button").filter(has_text="Add to cart")
            if add_button.is_visible():
                add_button.click()

    def remove_all_products_from_cart(self):
        """Remove all products from cart."""
        log_step("Removing all products from cart")
        count = self.get_product_count()
        for i in range(count):
            product = self.inventory_items.nth(i)
            remove_button = product.locator("button").filter(has_text="Remove")
            if remove_button.is_visible():
                remove_button.click()
