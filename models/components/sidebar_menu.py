"""
Sidebar menu component (burger menu).
"""

from playwright.sync_api import Page, expect
from utils.logger import log_step


class SidebarMenuComponent:
    """Reusable sidebar/burger menu component."""

    def __init__(self, page: Page):
        """
        Initialize sidebar menu component.

        Args:
            page: Playwright page instance
        """
        self.page = page

        # Menu container
        self.menu_container = page.locator(".bm-menu-wrap")
        self.menu_overlay = page.locator(".bm-overlay")

        # Menu items
        self.menu_item_list = page.locator(".bm-item-list")
        self.all_items_link = page.locator("#inventory_sidebar_link")
        self.about_link = page.locator("#about_sidebar_link")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.reset_app_link = page.locator("#reset_sidebar_link")

        # Close button
        self.close_button = page.locator("#react-burger-cross-btn")

    def is_open(self) -> bool:
        """
        Check if sidebar menu is open.

        Returns:
            True if menu is open, False otherwise
        """
        return self.menu_container.is_visible()

    def wait_for_menu_open(self, timeout: int = 3000):
        """
        Wait for menu to open.

        Args:
            timeout: Timeout in milliseconds
        """
        expect(self.menu_container).to_be_visible(timeout=timeout)
        # Wait for animation
        self.page.wait_for_timeout(300)

    def wait_for_menu_close(self, timeout: int = 3000):
        """
        Wait for menu to close.

        Args:
            timeout: Timeout in milliseconds
        """
        expect(self.menu_container).to_be_hidden(timeout=timeout)

    def click_all_items(self):
        """Click All Items link to go to inventory page."""
        log_step("Clicking All Items link")
        self.wait_for_menu_open()
        self.all_items_link.click()

    def click_about(self):
        """Click About link to go to Sauce Labs website."""
        log_step("Clicking About link")
        self.wait_for_menu_open()
        self.about_link.click()

    def click_logout(self):
        """Click Logout link to log out."""
        log_step("Clicking Logout link")
        self.wait_for_menu_open()
        self.logout_link.click()

    def click_reset_app_state(self):
        """Click Reset App State link to reset the application."""
        log_step("Clicking Reset App State link")
        self.wait_for_menu_open()
        self.reset_app_link.click()

    def close_menu(self):
        """Close the sidebar menu."""
        log_step("Closing sidebar menu")
        if self.is_open():
            self.close_button.click()
            self.wait_for_menu_close()

    def logout(self):
        """
        Perform logout action.
        Opens menu if needed and clicks logout.
        """
        log_step("Logging out")
        if not self.is_open():
            # Open menu first
            burger_button = self.page.locator("#react-burger-menu-btn")
            burger_button.click()
            self.wait_for_menu_open()

        self.click_logout()

    def reset_app_state(self):
        """
        Reset application state.
        Opens menu if needed and clicks reset.
        """
        log_step("Resetting app state")
        if not self.is_open():
            # Open menu first
            burger_button = self.page.locator("#react-burger-menu-btn")
            burger_button.click()
            self.wait_for_menu_open()

        self.click_reset_app_state()
        # Close menu after reset
        self.close_menu()

    def navigate_to_all_items(self):
        """
        Navigate to all items page.
        Opens menu if needed and clicks all items.
        """
        log_step("Navigating to all items")
        if not self.is_open():
            # Open menu first
            burger_button = self.page.locator("#react-burger-menu-btn")
            burger_button.click()
            self.wait_for_menu_open()

        self.click_all_items()

    def navigate_to_about(self):
        """
        Navigate to about page.
        Opens menu if needed and clicks about.
        """
        log_step("Navigating to about page")
        if not self.is_open():
            # Open menu first
            burger_button = self.page.locator("#react-burger-menu-btn")
            burger_button.click()
            self.wait_for_menu_open()

        self.click_about()

    def verify_all_menu_items_visible(self) -> bool:
        """
        Verify all menu items are visible.

        Returns:
            True if all items are visible, False otherwise
        """
        if not self.is_open():
            log_step("Menu is not open, cannot verify items")
            return False

        items_visible = (
            self.all_items_link.is_visible() and
            self.about_link.is_visible() and
            self.logout_link.is_visible() and
            self.reset_app_link.is_visible()
        )

        if not items_visible:
            log_step("Not all menu items are visible")
            return False

        return True

    def get_menu_item_text(self, item_name: str) -> str:
        """
        Get text of a specific menu item.

        Args:
            item_name: Name of menu item (all_items, about, logout, reset)

        Returns:
            Menu item text
        """
        items = {
            "all_items": self.all_items_link,
            "about": self.about_link,
            "logout": self.logout_link,
            "reset": self.reset_app_link
        }

        if item_name in items:
            return items[item_name].text_content() or ""
        return ""
