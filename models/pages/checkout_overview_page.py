"""
Checkout overview page object (Step 2 of checkout process).
"""

from typing import List, Dict, Any
from playwright.sync_api import Page, Locator
from models.base_page import BasePage
from utils.logger import logger, log_step


class CheckoutOverviewPage(BasePage):
    """Page object for the checkout overview page (step 2)."""

    def __init__(self, page: Page):
        """Initialize checkout overview page."""
        super().__init__(page, "/checkout-step-two.html")

        # Page title
        self.page_title = page.locator(".title")

        # Cart items
        self.cart_list = page.locator(".cart_list")
        self.cart_items = page.locator(".cart_item")

        # Summary information
        self.summary_info = page.locator(".summary_info")

        # Payment information
        self.payment_info_label = page.locator(".summary_info_label").filter(has_text="Payment Information")
        self.payment_info_value = page.locator("[data-test='payment-info-value']")

        # Shipping information
        self.shipping_info_label = page.locator(".summary_info_label").filter(has_text="Shipping Information")
        self.shipping_info_value = page.locator("[data-test='shipping-info-value']")

        # Price summary
        self.price_total_label = page.locator(".summary_info_label").filter(has_text="Price Total")
        self.subtotal_label = page.locator(".summary_subtotal_label")
        self.tax_label = page.locator(".summary_tax_label")
        self.total_label = page.locator(".summary_total_label")

        # Buttons
        self.cancel_button = page.locator("#cancel")
        self.finish_button = page.locator("#finish")

        # Cart
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def get_cart_items_count(self) -> int:
        """
        Get the number of items in checkout.

        Returns:
            Number of items
        """
        return self.cart_items.count()

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
        Get list of all product names in checkout.

        Returns:
            List of product names
        """
        names = []
        count = self.get_cart_items_count()
        for i in range(count):
            names.append(self.get_cart_item_name(i))
        return names

    def get_payment_information(self) -> str:
        """
        Get payment information.

        Returns:
            Payment information text
        """
        return self.payment_info_value.text_content() or ""

    def get_shipping_information(self) -> str:
        """
        Get shipping information.

        Returns:
            Shipping information text
        """
        return self.shipping_info_value.text_content() or ""

    def get_subtotal(self) -> float:
        """
        Get the subtotal amount.

        Returns:
            Subtotal as float
        """
        subtotal_text = self.subtotal_label.text_content() or "Item total: $0.00"
        # Extract the price from "Item total: $XX.XX"
        price_text = subtotal_text.split("$")[-1]
        return float(price_text)

    def get_tax(self) -> float:
        """
        Get the tax amount.

        Returns:
            Tax as float
        """
        tax_text = self.tax_label.text_content() or "Tax: $0.00"
        # Extract the price from "Tax: $X.XX"
        price_text = tax_text.split("$")[-1]
        return float(price_text)

    def get_total(self) -> float:
        """
        Get the total amount.

        Returns:
            Total as float
        """
        total_text = self.total_label.text_content() or "Total: $0.00"
        # Extract the price from "Total: $XX.XX"
        price_text = total_text.split("$")[-1]
        return float(price_text)

    def calculate_expected_subtotal(self) -> float:
        """
        Calculate expected subtotal from items.

        Returns:
            Expected subtotal
        """
        items = self.get_all_cart_items()
        subtotal = 0
        for item in items:
            subtotal += item["price"] * item["quantity"]
        return round(subtotal, 2)

    def calculate_expected_tax(self, tax_rate: float = 0.08) -> float:
        """
        Calculate expected tax.

        Args:
            tax_rate: Tax rate (default 8%)

        Returns:
            Expected tax amount
        """
        subtotal = self.calculate_expected_subtotal()
        return round(subtotal * tax_rate, 2)

    def calculate_expected_total(self, tax_rate: float = 0.08) -> float:
        """
        Calculate expected total.

        Args:
            tax_rate: Tax rate (default 8%)

        Returns:
            Expected total amount
        """
        subtotal = self.calculate_expected_subtotal()
        tax = self.calculate_expected_tax(tax_rate)
        return round(subtotal + tax, 2)

    def verify_totals(self, tax_rate: float = 0.08) -> bool:
        """
        Verify all totals are calculated correctly.

        Args:
            tax_rate: Tax rate (default 8%)

        Returns:
            True if all totals are correct, False otherwise
        """
        # Get actual values
        actual_subtotal = self.get_subtotal()
        actual_tax = self.get_tax()
        actual_total = self.get_total()

        # Calculate expected values
        expected_subtotal = self.calculate_expected_subtotal()
        expected_tax = self.calculate_expected_tax(tax_rate)
        expected_total = self.calculate_expected_total(tax_rate)

        # Verify subtotal
        if abs(actual_subtotal - expected_subtotal) > 0.01:
            logger.error("Subtotal mismatch. Expected: $%s, Actual: $%s",
                        expected_subtotal, actual_subtotal)
            return False

        # Verify tax
        if abs(actual_tax - expected_tax) > 0.01:
            logger.error("Tax mismatch. Expected: $%s, Actual: $%s",
                        expected_tax, actual_tax)
            return False

        # Verify total
        if abs(actual_total - expected_total) > 0.01:
            logger.error("Total mismatch. Expected: $%s, Actual: $%s",
                        expected_total, actual_total)
            return False

        logger.info("All totals verified: Subtotal=$%s, Tax=$%s, Total=$%s",
                    actual_subtotal, actual_tax, actual_total)
        return True

    def click_finish(self):
        """Click Finish button to complete order."""
        log_step("Clicking Finish button to complete order")
        self.finish_button.click()
        self.page.wait_for_url("**/checkout-complete.html", wait_until="networkidle")

    def click_cancel(self):
        """Click Cancel button to go back."""
        log_step("Clicking Cancel button")
        self.cancel_button.click()

    def complete_order(self):
        """Alias for click_finish()."""
        self.click_finish()

    def cancel_order(self):
        """Alias for click_cancel()."""
        self.click_cancel()

    def verify_items_in_checkout(self, expected_items: List[str]) -> bool:
        """
        Verify expected items are in checkout.

        Args:
            expected_items: List of expected product names

        Returns:
            True if all expected items are present, False otherwise
        """
        actual_items = self.get_all_cart_item_names()
        for expected_item in expected_items:
            if expected_item not in actual_items:
                logger.error("Expected item '%s' not found in checkout", expected_item)
                return False
        return True

    def get_summary_details(self) -> Dict[str, Any]:
        """
        Get complete summary details.

        Returns:
            Dictionary with all summary information
        """
        return {
            "items": self.get_all_cart_items(),
            "payment_info": self.get_payment_information(),
            "shipping_info": self.get_shipping_information(),
            "subtotal": self.get_subtotal(),
            "tax": self.get_tax(),
            "total": self.get_total()
        }

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
