"""
Enhanced Base Page class with utilities for all page objects.
"""

from typing import List, Any, Optional
from playwright.sync_api import Page, Locator
from utils.logger import logger, log_step
from utils.wait_helpers import WaitHelpers
from utils.assertion_helpers import AssertionHelpers
from utils.screenshot_helper import ScreenshotHelper


class BasePage:
    """Base page class with common functionality for all page objects."""

    def __init__(self, page: Page, url: str):
        """
        Initialize base page.

        Args:
            page: Playwright page instance
            url: Page URL
        """
        self.page = page
        self.url = url
        self.wait = WaitHelpers(page)
        self.assert_that = AssertionHelpers(page)
        self.screenshot = ScreenshotHelper(page)

    def open(self):
        """Navigate to the page URL."""
        log_step(f"Opening page: {self.url}")
        self.page.goto(self.url)
        self.wait.wait_for_load_state()

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Get current page URL."""
        return self.page.url

    def refresh(self):
        """Refresh the current page."""
        log_step("Refreshing page")
        self.page.reload()
        self.wait.wait_for_load_state()

    def go_back(self):
        """Navigate back in browser history."""
        log_step("Navigating back")
        self.page.go_back()
        self.wait.wait_for_load_state()

    def go_forward(self):
        """Navigate forward in browser history."""
        log_step("Navigating forward")
        self.page.go_forward()
        self.wait.wait_for_load_state()

    # Element interaction methods
    def click(self, selector: str, timeout: Optional[int] = None):
        """
        Click an element.

        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
        """
        log_step(f"Clicking element: {selector}")
        element = self.wait.wait_for_element(selector, timeout=timeout)
        element.click()

    def double_click(self, selector: str, timeout: Optional[int] = None):
        """
        Double-click an element.

        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
        """
        log_step(f"Double-clicking element: {selector}")
        element = self.wait.wait_for_element(selector, timeout=timeout)
        element.dblclick()

    def right_click(self, selector: str, timeout: Optional[int] = None):
        """
        Right-click an element.

        Args:
            selector: Element selector
            timeout: Optional timeout in milliseconds
        """
        log_step(f"Right-clicking element: {selector}")
        element = self.wait.wait_for_element(selector, timeout=timeout)
        element.click(button="right")

    def type_text(
        self,
        selector: str,
        text: str,
        clear: bool = True,
        timeout: Optional[int] = None
    ):
        log_step(f"Typing text into {selector}: {text}")
        element = self.wait.wait_for_element(selector, timeout=timeout)

        if clear:
            element.clear()

        element.fill(text)

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        element = self.wait.wait_for_element(selector, timeout=timeout)
        return element.text_content() or ""

    def get_attribute(
        self,
        selector: str,
        attribute: str,
        timeout: Optional[int] = None
    ) -> Optional[str]:
        element = self.wait.wait_for_element(selector, timeout=timeout)
        return element.get_attribute(attribute)

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        try:
            self.wait.wait_for_element(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def is_enabled(self, selector: str, timeout: int = 5000) -> bool:
        try:
            element = self.wait.wait_for_element(selector, timeout=timeout)
            return element.is_enabled()
        except Exception:
            return False

    def is_checked(self, selector: str, timeout: int = 5000) -> bool:
        try:
            element = self.wait.wait_for_element(selector, timeout=timeout)
            return element.is_checked()
        except Exception:
            return False

    def select_option(self, selector: str, value: str, by: str = "value", timeout: Optional[int] = None):
        log_step(f"Selecting option {value} from {selector}")
        element = self.wait.wait_for_element(selector, timeout=timeout)

        if by == "value":
            element.select_option(value=value)
        elif by == "label":
            element.select_option(label=value)
        elif by == "index":
            element.select_option(index=int(value))

    def hover(self, selector: str, timeout: Optional[int] = None):
        log_step(f"Hovering over element: {selector}")
        element = self.wait.wait_for_element(selector, timeout=timeout)
        element.hover()

    def scroll_to_element(self, selector: str, timeout: Optional[int] = None):
        log_step(f"Scrolling to element: {selector}")
        element = self.wait.wait_for_element(selector, timeout=timeout)
        element.scroll_into_view_if_needed()

    def get_elements(self, selector: str) -> List[Locator]:
        return self.page.locator(selector).all()

    def get_element_count(self, selector: str) -> int:
        return self.page.locator(selector).count()

    def execute_javascript(self, script: str, *args) -> Any:
        logger.debug("Executing JavaScript: %s...", script[:50])
        return self.page.evaluate(script, *args)

    def wait_for_navigation(self, timeout: Optional[int] = None):
        log_step("Waiting for navigation")
        self.wait.wait_for_load_state("networkidle", timeout=timeout)

    def close_popup(self, selector: str = "[aria-label='Close']"):
        if self.is_visible(selector, timeout=2000):
            log_step("Closing popup")
            self.click(selector)

    def switch_to_frame(self, selector: str):
        log_step(f"Switching to frame: {selector}")
        frame = self.page.frame_locator(selector)
        return frame

    def capture_screenshot(self, name: Optional[str] = None) -> str:
        return self.screenshot.capture_screenshot(name)
