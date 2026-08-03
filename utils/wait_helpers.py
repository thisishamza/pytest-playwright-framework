"""
Custom wait conditions and helpers for Playwright tests.
"""

from typing import Optional, Callable
from playwright.sync_api import Page, Locator, expect
from utils.logger import logger


class WaitHelpers:
    """Custom wait conditions for Playwright tests."""

    def __init__(self, page: Page, timeout: int = 30000):
        """
        Initialize wait helpers.

        Args:
            page: Playwright page instance
            timeout: Default timeout in milliseconds
        """
        self.page = page
        self.timeout = timeout

    def wait_for_element(
        self,
        selector: str,
        state: str = "visible",
        timeout: Optional[int] = None
    ) -> Locator:
        """
        Wait for an element to reach a specific state.

        Args:
            selector: Element selector
            state: Element state (visible, hidden, attached, detached)
            timeout: Custom timeout in milliseconds

        Returns:
            Locator for the element
        """
        timeout = timeout or self.timeout
        locator = self.page.locator(selector)

        logger.debug(f"Waiting for element {selector} to be {state}")
        locator.wait_for(state=state, timeout=timeout)

        return locator

    def wait_for_text(
        self,
        text: str,
        selector: Optional[str] = None,
        timeout: Optional[int] = None
    ):
        """
        Wait for specific text to appear on the page.

        Args:
            text: Text to wait for
            selector: Optional selector to search within
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout

        if selector:
            locator = self.page.locator(selector)
            expect(locator).to_contain_text(text, timeout=timeout)
        else:
            expect(self.page).to_have_text(text, timeout=timeout)

        logger.debug(f"Text '{text}' found on page")

    def wait_for_url(
        self,
        url_pattern: str,
        timeout: Optional[int] = None
    ):
        """
        Wait for the page URL to match a pattern.

        Args:
            url_pattern: URL pattern (can be regex)
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout

        logger.debug(f"Waiting for URL to match: {url_pattern}")
        self.page.wait_for_url(url_pattern, timeout=timeout)

    def wait_for_load_state(
        self,
        state: str = "networkidle",
        timeout: Optional[int] = None
    ):
        """
        Wait for page to reach specific load state.

        Args:
            state: Load state (load, domcontentloaded, networkidle)
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout

        logger.debug(f"Waiting for page load state: {state}")
        self.page.wait_for_load_state(state, timeout=timeout)

    def wait_for_element_count(
        self,
        selector: str,
        count: int,
        timeout: Optional[int] = None
    ):
        """
        Wait for specific number of elements to be present.

        Args:
            selector: Element selector
            count: Expected number of elements
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout

        logger.debug(f"Waiting for {count} elements matching {selector}")
        expect(self.page.locator(selector)).to_have_count(count, timeout=timeout)

    def wait_for_element_to_be_enabled(
        self,
        selector: str,
        timeout: Optional[int] = None
    ) -> Locator:
        """
        Wait for an element to be enabled.

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            Locator for the enabled element
        """
        timeout = timeout or self.timeout
        locator = self.page.locator(selector)

        logger.debug(f"Waiting for element {selector} to be enabled")
        expect(locator).to_be_enabled(timeout=timeout)

        return locator

    def wait_for_element_to_be_disabled(
        self,
        selector: str,
        timeout: Optional[int] = None
    ) -> Locator:
        """
        Wait for an element to be disabled.

        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds

        Returns:
            Locator for the disabled element
        """
        timeout = timeout or self.timeout
        locator = self.page.locator(selector)

        logger.debug(f"Waiting for element {selector} to be disabled")
        expect(locator).to_be_disabled(timeout=timeout)

        return locator

    def wait_for_animation(self, duration: int = 500):
        """
        Wait for animations to complete.

        Args:
            duration: Wait duration in milliseconds
        """
        logger.debug(f"Waiting {duration}ms for animations to complete")
        self.page.wait_for_timeout(duration)

    def wait_for_function(
        self,
        expression: str,
        timeout: Optional[int] = None
    ):
        """
        Wait for a JavaScript function to return true.

        Args:
            expression: JavaScript expression to evaluate
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout

        logger.debug(f"Waiting for JavaScript expression: {expression}")
        self.page.wait_for_function(expression, timeout=timeout)

    def wait_until_element_stops_moving(
        self,
        selector: str,
        timeout: Optional[int] = None,
        check_interval: int = 100
    ):
        """
        Wait until an element stops moving (useful for animations).

        Args:
            selector: Element selector
            timeout: Maximum wait time in milliseconds
            check_interval: Interval between position checks
        """
        timeout = timeout or self.timeout

        logger.debug(f"Waiting for element {selector} to stop moving")

        # JavaScript to check element position
        js_expression = f"""
            () => {{
                const element = document.querySelector('{selector}');
                if (!element) return false;

                const rect1 = element.getBoundingClientRect();
                return new Promise(resolve => {{
                    setTimeout(() => {{
                        const rect2 = element.getBoundingClientRect();
                        resolve(rect1.top === rect2.top && rect1.left === rect2.left);
                    }}, {check_interval});
                }});
            }}
        """

        self.page.wait_for_function(js_expression, timeout=timeout)