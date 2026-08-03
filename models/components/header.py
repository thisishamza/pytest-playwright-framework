"""
Header component that appears on all pages.
"""

from playwright.sync_api import Page
from utils.logger import log_step


class HeaderComponent:
    """Reusable header component."""

    def __init__(self, page: Page):
        """
        Initialize header component.

        Args:
            page: Playwright page instance
        """
        self.page = page

        # Header container
        self.header_container = page.locator(".header_container")

        # Menu button
        self.burger_menu_button = page.locator("#react-burger-menu-btn")

        # Logo
        self.app_logo = page.locator(".app_logo")

        # Page title (changes based on current page)
        self.header_title = page.locator(".header_secondary_container .title")

        # Shopping cart
        self.shopping_cart_container = page.locator("#shopping_cart_container")
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def is_visible(self) -> bool:
        """
        Check if header is visible.

        Returns:
            True if header is visible, False otherwise
        """
        return self.header_container.is_visible()

    def get_page_title(self) -> str:
        """
        Get the current page title from header.

        Returns:
            Page title text
        """
        if self.header_title.is_visible():
            return self.header_title.text_content() or ""
        return ""

    def get_cart_count(self) -> int:
        """
        Get the number of items in cart from badge.

        Returns:
            Number of items in cart, 0 if badge not visible
        """
        if self.cart_badge.is_visible():
            count_text = self.cart_badge.text_content() or "0"
            return int(count_text)
        return 0

    def is_cart_badge_visible(self) -> bool:
        """
        Check if cart badge is visible.

        Returns:
            True if cart badge is visible, False otherwise
        """
        return self.cart_badge.is_visible()

    def click_cart(self):
        """Navigate to shopping cart."""
        log_step("Clicking shopping cart")
        self.shopping_cart_link.click()

    def click_menu_button(self):
        """Open the burger menu."""
        log_step("Clicking burger menu button")
        self.burger_menu_button.click()

    def is_menu_button_visible(self) -> bool:
        """
        Check if menu button is visible.

        Returns:
            True if menu button is visible, False otherwise
        """
        return self.burger_menu_button.is_visible()

    def is_logo_visible(self) -> bool:
        """
        Check if app logo is visible.

        Returns:
            True if logo is visible, False otherwise
        """
        return self.app_logo.is_visible()

    def verify_cart_count(self, expected_count: int) -> bool:
        """
        Verify cart has expected number of items.

        Args:
            expected_count: Expected number of items

        Returns:
            True if count matches, False otherwise
        """
        actual_count = self.get_cart_count()
        if actual_count != expected_count:
            log_step(f"Cart count mismatch. Expected: {expected_count}, Actual: {actual_count}")
            return False
        return True

    def wait_for_cart_update(self, timeout: int = 2000):
        """
        Wait for cart badge to update.

        Args:
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_timeout(timeout)
