"""
Checkout information page object (Step 1 of checkout process).
"""

from playwright.sync_api import Page
from models.base_page import BasePage
from utils.logger import logger, log_step


class CheckoutInfoPage(BasePage):
    """Page object for the checkout information page (step 1)."""

    def __init__(self, page: Page):
        """Initialize checkout info page."""
        super().__init__(page, "/checkout-step-one.html")

        # Page title
        self.page_title = page.locator(".title")

        # Form fields
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.postal_code_input = page.locator("#postal-code")

        # Error message
        self.error_message_container = page.locator(".error-message-container")
        self.error_message = page.locator("[data-test='error']")
        self.error_button = page.locator(".error-button")

        # Buttons
        self.cancel_button = page.locator("#cancel")
        self.continue_button = page.locator("#continue")

        # Cart
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def fill_checkout_form(
        self,
        first_name: str,
        last_name: str,
        postal_code: str
    ):
        """
        Fill the checkout form with provided information.

        Args:
            first_name: First name
            last_name: Last name
            postal_code: Postal/ZIP code
        """
        log_step(f"Filling checkout form: {first_name} {last_name}, {postal_code}")

        if first_name:
            self.first_name_input.fill(first_name)
        if last_name:
            self.last_name_input.fill(last_name)
        if postal_code:
            self.postal_code_input.fill(postal_code)

    def enter_first_name(self, first_name: str):
        """
        Enter first name.

        Args:
            first_name: First name to enter
        """
        log_step(f"Entering first name: {first_name}")
        self.first_name_input.fill(first_name)

    def enter_last_name(self, last_name: str):
        """
        Enter last name.

        Args:
            last_name: Last name to enter
        """
        log_step(f"Entering last name: {last_name}")
        self.last_name_input.fill(last_name)

    def enter_postal_code(self, postal_code: str):
        """
        Enter postal code.

        Args:
            postal_code: Postal code to enter
        """
        log_step(f"Entering postal code: {postal_code}")
        self.postal_code_input.fill(postal_code)

    def get_first_name(self) -> str:
        """
        Get the value in first name field.

        Returns:
            First name value
        """
        return self.first_name_input.input_value()

    def get_last_name(self) -> str:
        """
        Get the value in last name field.

        Returns:
            Last name value
        """
        return self.last_name_input.input_value()

    def get_postal_code(self) -> str:
        """
        Get the value in postal code field.

        Returns:
            Postal code value
        """
        return self.postal_code_input.input_value()

    def clear_form(self):
        """Clear all form fields."""
        log_step("Clearing checkout form")
        self.first_name_input.clear()
        self.last_name_input.clear()
        self.postal_code_input.clear()

    def click_continue(self):
        """Click Continue button to proceed to next step."""
        log_step("Clicking Continue button")
        self.continue_button.click()

    def click_cancel(self):
        """Click Cancel button to go back to cart."""
        log_step("Clicking Cancel button")
        self.cancel_button.click()

    def continue_checkout(self):
        """Alias for click_continue()."""
        self.click_continue()

    def cancel_checkout(self):
        """Alias for click_cancel()."""
        self.click_cancel()

    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error is displayed, False otherwise
        """
        return self.error_message_container.is_visible()

    def get_error_message(self) -> str:
        """
        Get the error message text.

        Returns:
            Error message text, empty string if no error
        """
        if self.is_error_displayed():
            return self.error_message.text_content() or ""
        return ""

    def close_error_message(self):
        """Close the error message if displayed."""
        if self.is_error_displayed():
            log_step("Closing error message")
            self.error_button.click()

    def is_first_name_required(self) -> bool:
        """
        Check if first name field is required.

        Returns:
            True if field is required
        """
        return self.first_name_input.get_attribute("required") == "true"

    def is_last_name_required(self) -> bool:
        """
        Check if last name field is required.

        Returns:
            True if field is required
        """
        return self.last_name_input.get_attribute("required") == "true"

    def is_postal_code_required(self) -> bool:
        """
        Check if postal code field is required.

        Returns:
            True if field is required
        """
        return self.postal_code_input.get_attribute("required") == "true"

    def submit_empty_form(self):
        """Submit form with all fields empty."""
        log_step("Submitting empty checkout form")
        self.clear_form()
        self.click_continue()

    def submit_form_missing_first_name(self, last_name: str, postal_code: str):
        """
        Submit form with missing first name.

        Args:
            last_name: Last name to enter
            postal_code: Postal code to enter
        """
        log_step("Submitting form without first name")
        self.clear_form()
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        self.click_continue()

    def submit_form_missing_last_name(self, first_name: str, postal_code: str):
        """
        Submit form with missing last name.

        Args:
            first_name: First name to enter
            postal_code: Postal code to enter
        """
        log_step("Submitting form without last name")
        self.clear_form()
        self.enter_first_name(first_name)
        self.enter_postal_code(postal_code)
        self.click_continue()

    def submit_form_missing_postal_code(self, first_name: str, last_name: str):
        """
        Submit form with missing postal code.

        Args:
            first_name: First name to enter
            last_name: Last name to enter
        """
        log_step("Submitting form without postal code")
        self.clear_form()
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.click_continue()

    def verify_error_for_empty_field(self, field_name: str) -> bool:
        """
        Verify error message for empty field.

        Args:
            field_name: Name of the field (first_name, last_name, postal_code)

        Returns:
            True if correct error is displayed, False otherwise
        """
        expected_errors = {
            "first_name": "Error: First Name is required",
            "last_name": "Error: Last Name is required",
            "postal_code": "Error: Postal Code is required"
        }

        expected_error = expected_errors.get(field_name, "")
        actual_error = self.get_error_message()

        if actual_error != expected_error:
            logger.error("Error message mismatch. Expected: %s, Actual: %s",
                        expected_error, actual_error)
            return False
        return True

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

    def complete_step_with_valid_data(
        self,
        first_name: str = "Test",
        last_name: str = "User",
        postal_code: str = "12345"
    ):
        """
        Complete this checkout step with valid data and continue.

        Args:
            first_name: First name (default: Test)
            last_name: Last name (default: User)
            postal_code: Postal code (default: 12345)
        """
        self.fill_checkout_form(first_name, last_name, postal_code)
        self.click_continue()
