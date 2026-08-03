"""
Custom assertion helpers for enhanced test validation.
"""

from typing import List, Optional, Any
from playwright.sync_api import Page, Locator, expect
from utils.logger import logger


class AssertionHelpers:
    """Enhanced assertion methods for tests."""

    def __init__(self, page: Page):
        """
        Initialize assertion helpers.

        Args:
            page: Playwright page instance
        """
        self.page = page
        self.soft_errors: List[str] = []

    def assert_element_visible(self, selector: str, message: Optional[str] = None):
        """
        Assert that an element is visible.

        Args:
            selector: Element selector
            message: Custom assertion message
        """
        message = message or f"Element {selector} should be visible"
        logger.debug(f"Asserting: {message}")

        locator = self.page.locator(selector)
        expect(locator).to_be_visible()

    def assert_element_hidden(self, selector: str, message: Optional[str] = None):
        """
        Assert that an element is hidden.

        Args:
            selector: Element selector
            message: Custom assertion message
        """
        message = message or f"Element {selector} should be hidden"
        logger.debug(f"Asserting: {message}")

        locator = self.page.locator(selector)
        expect(locator).to_be_hidden()

    def assert_text_present(
        self,
        text: str,
        selector: Optional[str] = None,
        message: Optional[str] = None
    ):
        """
        Assert that specific text is present.

        Args:
            text: Text to find
            selector: Optional selector to search within
            message: Custom assertion message
        """
        message = message or f"Text '{text}' should be present"
        logger.debug(f"Asserting: {message}")

        if selector:
            locator = self.page.locator(selector)
            expect(locator).to_contain_text(text)
        else:
            expect(self.page).to_have_text(text)

    def assert_element_count(
        self,
        selector: str,
        expected_count: int,
        message: Optional[str] = None
    ):
        """
        Assert the number of elements matching a selector.

        Args:
            selector: Element selector
            expected_count: Expected number of elements
            message: Custom assertion message
        """
        message = message or f"Expected {expected_count} elements matching {selector}"
        logger.debug(f"Asserting: {message}")

        locator = self.page.locator(selector)
        expect(locator).to_have_count(expected_count)

    def assert_element_enabled(self, selector: str, message: Optional[str] = None):
        """
        Assert that an element is enabled.

        Args:
            selector: Element selector
            message: Custom assertion message
        """
        message = message or f"Element {selector} should be enabled"
        logger.debug(f"Asserting: {message}")

        locator = self.page.locator(selector)
        expect(locator).to_be_enabled()

    def assert_element_disabled(self, selector: str, message: Optional[str] = None):
        """
        Assert that an element is disabled.

        Args:
            selector: Element selector
            message: Custom assertion message
        """
        message = message or f"Element {selector} should be disabled"
        logger.debug(f"Asserting: {message}")

        locator = self.page.locator(selector)
        expect(locator).to_be_disabled()

    def assert_url_contains(self, expected_url: str, message: Optional[str] = None):
        """
        Assert that the current URL contains expected text.

        Args:
            expected_url: Expected URL or URL fragment
            message: Custom assertion message
        """
        message = message or f"URL should contain '{expected_url}'"
        logger.debug(f"Asserting: {message}")

        expect(self.page).to_have_url(expected_url)

    def assert_title_contains(self, expected_title: str, message: Optional[str] = None):
        """
        Assert that the page title contains expected text.

        Args:
            expected_title: Expected title text
            message: Custom assertion message
        """
        message = message or f"Title should contain '{expected_title}'"
        logger.debug(f"Asserting: {message}")

        expect(self.page).to_have_title(expected_title)

    def assert_attribute_value(
        self,
        selector: str,
        attribute: str,
        expected_value: str,
        message: Optional[str] = None
    ):
        """
        Assert that an element has a specific attribute value.

        Args:
            selector: Element selector
            attribute: Attribute name
            expected_value: Expected attribute value
            message: Custom assertion message
        """
        message = message or f"Element {selector} should have {attribute}='{expected_value}'"
        logger.debug(f"Asserting: {message}")

        locator = self.page.locator(selector)
        expect(locator).to_have_attribute(attribute, expected_value)

    def assert_checkbox_checked(self, selector: str, message: Optional[str] = None):
        """
        Assert that a checkbox is checked.

        Args:
            selector: Checkbox selector
            message: Custom assertion message
        """
        message = message or f"Checkbox {selector} should be checked"
        logger.debug(f"Asserting: {message}")

        locator = self.page.locator(selector)
        expect(locator).to_be_checked()

    def assert_checkbox_unchecked(self, selector: str, message: Optional[str] = None):
        """
        Assert that a checkbox is unchecked.

        Args:
            selector: Checkbox selector
            message: Custom assertion message
        """
        message = message or f"Checkbox {selector} should be unchecked"
        logger.debug(f"Asserting: {message}")

        locator = self.page.locator(selector)
        expect(locator).not_to_be_checked()

    # Soft assertions
    def soft_assert(self, condition: bool, message: str):
        """
        Perform a soft assertion that doesn't stop test execution.

        Args:
            condition: Condition to check
            message: Error message if condition is False
        """
        if not condition:
            self.soft_errors.append(message)
            logger.warning(f"Soft assertion failed: {message}")

    def assert_all_soft_assertions(self):
        """
        Check all soft assertions and fail if any errors were recorded.
        """
        if self.soft_errors:
            error_message = "\n".join(self.soft_errors)
            self.soft_errors.clear()
            raise AssertionError(f"Soft assertions failed:\n{error_message}")

    def assert_greater_than(
        self,
        actual: Any,
        expected: Any,
        message: Optional[str] = None
    ):
        """
        Assert that actual value is greater than expected.

        Args:
            actual: Actual value
            expected: Expected value
            message: Custom assertion message
        """
        message = message or f"{actual} should be greater than {expected}"
        logger.debug(f"Asserting: {message}")

        assert actual > expected, message

    def assert_less_than(
        self,
        actual: Any,
        expected: Any,
        message: Optional[str] = None
    ):
        """
        Assert that actual value is less than expected.

        Args:
            actual: Actual value
            expected: Expected value
            message: Custom assertion message
        """
        message = message or f"{actual} should be less than {expected}"
        logger.debug(f"Asserting: {message}")

        assert actual < expected, message

    def assert_list_equals(
        self,
        actual_list: List[Any],
        expected_list: List[Any],
        message: Optional[str] = None
    ):
        """
        Assert that two lists are equal.

        Args:
            actual_list: Actual list
            expected_list: Expected list
            message: Custom assertion message
        """
        message = message or f"Lists should be equal"
        logger.debug(f"Asserting: {message}")

        assert actual_list == expected_list, f"{message}\nActual: {actual_list}\nExpected: {expected_list}"

    def assert_list_contains(
        self,
        list_to_check: List[Any],
        item: Any,
        message: Optional[str] = None
    ):
        """
        Assert that a list contains a specific item.

        Args:
            list_to_check: List to check
            item: Item to find in list
            message: Custom assertion message
        """
        message = message or f"List should contain '{item}'"
        logger.debug(f"Asserting: {message}")

        assert item in list_to_check, f"{message}\nList: {list_to_check}"