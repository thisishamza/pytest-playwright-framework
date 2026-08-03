from playwright.sync_api import Page
from models.base_page import BasePage
from utils.logger import logger, log_step


class LoginPage(BasePage):

    def __init__(self, page: Page, url: str = ''):
        super().__init__(page, url)
        self.login_logo = page.locator('[class="login_logo"]')
        self.login_container = page.locator('.login_container')
        self.username_input = page.locator('#user-name')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('#login-button')
        self.error_message_container = page.locator('.error-message-container')
        self.error_message = page.locator('[data-test="error"]')
        self.error_button = page.locator('.error-button')
        self.login_credentials = page.locator('.login_credentials_wrap')
        self.accepted_usernames = page.locator('#login_credentials')
        self.password_info = page.locator('.login_password')

    def enter_username(self, username: str):
        """
        Enter username.

        Args:
            username: Username to enter
        """
        log_step(f"Entering username: {username}")
        self.username_input.fill(username)

    def enter_password(self, password: str):
        """
        Enter password.

        Args:
            password: Password to enter
        """
        log_step("Entering password")
        self.password_input.fill(password)

    def click_login(self):
        """Click login button."""
        log_step("Clicking login button")
        self.login_button.click()

    def login(self, username: str, password: str):
        """
        Perform login with given credentials.

        Args:
            username: Username
            password: Password
        """
        log_step(f"Logging in with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error is displayed, False otherwise
        """
        # Check if error button is visible (more reliable than container)
        # The container might stay visible but empty after closing
        return self.error_button.is_visible()

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
            # Wait for error button to be hidden (indicates message is closed)
            # On Saucedemo, the container stays but the button/content disappears
            self.error_button.wait_for(state="hidden", timeout=3000)

    def is_login_logo_visible(self) -> bool:
        """
        Check if login logo is visible.

        Returns:
            True if logo is visible, False otherwise
        """
        return self.login_logo.is_visible()

    def is_at_login_page(self) -> bool:
        """
        Check if currently at login page.

        Returns:
            True if at login page, False otherwise
        """
        return self.login_container.is_visible() and self.login_button.is_visible()

    def get_accepted_usernames_text(self) -> str:
        """
        Get the accepted usernames text.

        Returns:
            Accepted usernames text
        """
        return self.accepted_usernames.text_content() or ""

    def get_password_info_text(self) -> str:
        """
        Get the password info text.

        Returns:
            Password info text
        """
        return self.password_info.text_content() or ""

    def clear_credentials(self):
        """Clear username and password fields."""
        log_step("Clearing login credentials")
        self.username_input.clear()
        self.password_input.clear()

    def login_with_enter_key(self, username: str, password: str):
        """
        Login by pressing Enter key instead of clicking button.

        Args:
            username: Username
            password: Password
        """
        log_step(f"Logging in with Enter key, username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.password_input.press("Enter")

    def wait_for_error_message(self, timeout: int = 5000):
        """
        Wait for error message to appear.

        Args:
            timeout: Timeout in milliseconds
        """
        self.wait.wait_for_element('[data-test="error"]', timeout=timeout)

    def verify_login_successful(self) -> bool:
        """
        Verify login was successful by checking we're not on login page.

        Returns:
            True if login successful, False otherwise
        """
        # Wait a bit for navigation
        self.wait.wait_for_animation(1000)

        # Check if we're still on login page
        if self.is_at_login_page():
            logger.error("Login failed - still on login page")
            return False

        # Check URL changed from login page
        current_url = self.page.url
        if current_url == self.url or current_url.endswith("/"):
            logger.error("Login failed - URL didn't change: %s", current_url)
            return False

        logger.info("Login successful")
        return True
