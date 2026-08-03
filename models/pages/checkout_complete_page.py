"""
Checkout complete page object (Order confirmation page).
"""

from playwright.sync_api import Page
from models.base_page import BasePage
from utils.logger import logger, log_step


class CheckoutCompletePage(BasePage):
    """Page object for the checkout complete/confirmation page."""

    def __init__(self, page: Page):
        """Initialize checkout complete page."""
        super().__init__(page, "/checkout-complete.html")

        # Page title
        self.page_title = page.locator(".title")

        # Checkout complete container
        self.checkout_complete_container = page.locator("#checkout_complete_container")

        # Success message elements
        self.success_image = page.locator(".pony_express")
        self.complete_header = page.locator(".complete-header")
        self.complete_text = page.locator(".complete-text")

        # Back button
        self.back_home_button = page.locator("#back-to-products")

        # Header elements (for consistency)
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.burger_menu_button = page.locator("#react-burger-menu-btn")

    def get_confirmation_header(self) -> str:
        """
        Get the confirmation header text.

        Returns:
            Confirmation header text
        """
        return self.complete_header.text_content() or ""

    def get_confirmation_text(self) -> str:
        """
        Get the confirmation message text.

        Returns:
            Confirmation message text
        """
        return self.complete_text.text_content() or ""

    def is_success_image_visible(self) -> bool:
        """
        Check if success image (pony) is visible.

        Returns:
            True if image is visible, False otherwise
        """
        try:
            # Wait for the success image to be visible with a short timeout
            self.success_image.wait_for(state="visible", timeout=3000)
            return True
        except Exception:
            return False

    def is_order_complete(self) -> bool:
        """
        Check if order completion is successful.

        Returns:
            True if order is complete, False otherwise
        """
        try:
            self.wait_for_page_load()
            return (
                self.checkout_complete_container.is_visible() and
                self.complete_header.is_visible() and
                self.is_success_image_visible()
            )
        except Exception:
            return False

    def click_back_home(self):
        """Click Back Home button to return to products page."""
        log_step("Clicking Back Home button")
        self.back_home_button.click()

    def go_back_to_products(self):
        """Alias for click_back_home()."""
        self.click_back_home()

    def verify_order_success(self) -> bool:
        """
        Verify order was successfully placed.

        Returns:
            True if order success is confirmed, False otherwise
        """
        expected_header = "Thank you for your order!"
        expected_text_partial = "Your order has been dispatched"

        actual_header = self.get_confirmation_header()
        actual_text = self.get_confirmation_text()

        # Check header
        if actual_header != expected_header:
            logger.error("Header mismatch. Expected: %s, Actual: %s",
                        expected_header, actual_header)
            return False

        # Check if text contains expected partial text
        if expected_text_partial not in actual_text:
            logger.error("Confirmation text doesn't contain expected text: %s", expected_text_partial)
            return False

        # Check if success image is visible
        if not self.is_success_image_visible():
            logger.error("Success image (pony) is not visible")
            return False

        logger.info("Order successfully completed and verified")
        return True

    def get_cart_count(self) -> int:
        """
        Get the number shown in cart badge.
        Should be 0 after order completion.

        Returns:
            Cart item count, 0 if badge not visible
        """
        if self.cart_badge.is_visible():
            count_text = self.cart_badge.text_content() or "0"
            return int(count_text)
        return 0

    def verify_cart_is_empty(self) -> bool:
        """
        Verify cart is empty after order completion.

        Returns:
            True if cart is empty, False otherwise
        """
        cart_count = self.get_cart_count()
        if cart_count != 0:
            logger.error("Cart should be empty after order completion but has %s items", cart_count)
            return False
        return True

    def open_menu(self):
        """Open the burger menu."""
        log_step("Opening burger menu")
        self.burger_menu_button.click()
        # Wait for menu animation
        self.wait.wait_for_animation(300)

    def wait_for_page_load(self):
        """Wait for checkout complete page to load."""
        self.wait.wait_for_element(".complete-header", timeout=5000)
        self.wait.wait_for_element(".pony_express", timeout=5000)
        # Also wait for the container to be stable
        self.page.wait_for_load_state("networkidle")
