"""
Negative login test cases for Saucedemo application.
Tests failed login scenarios and error handling.
"""

import pytest
import allure
from playwright.sync_api import expect
from data.test_data import TestData


@allure.feature("Authentication")
@allure.story("Login - Negative Cases")
class TestLoginNegative:
    """Negative login test cases."""

    @pytest.mark.auth
    @pytest.mark.negative
    @pytest.mark.smoke
    @allure.title("Login with locked out user")
    @allure.description("Verify appropriate error message for locked_out_user")
    def test_login_locked_out_user(self, login_page, locked_out_user):
        """Test login attempt with locked out user."""
        # Navigate to login page
        login_page.open()

        # Attempt login
        login_page.login(locked_out_user["username"], locked_out_user["password"])

        # Verify error message is displayed
        assert login_page.is_error_displayed(), "Error message not displayed"

        # Verify specific error message
        error_message = login_page.get_error_message()
        assert error_message == locked_out_user["error_message"], \
            f"Expected error: {locked_out_user['error_message']}, Got: {error_message}"

        # Verify still on login page
        assert login_page.is_at_login_page(), "Should remain on login page"

    @pytest.mark.auth
    @pytest.mark.negative
    @allure.title("Login with invalid username")
    @allure.description("Verify error message for non-existent username")
    def test_login_invalid_username(self, login_page):
        """Test login with invalid username."""
        # Navigate to login page
        login_page.open()

        # Attempt login with invalid username
        login_page.login("invalid_user", "secret_sauce")

        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_message = login_page.get_error_message()
        assert error_message == TestData.INVALID_CREDENTIALS_ERROR, \
            f"Unexpected error message: {error_message}"

        # Verify still on login page
        assert login_page.is_at_login_page(), "Should remain on login page"

    @pytest.mark.auth
    @pytest.mark.negative
    @allure.title("Login with invalid password")
    @allure.description("Verify error message for incorrect password")
    def test_login_invalid_password(self, login_page, standard_user):
        """Test login with invalid password."""
        # Navigate to login page
        login_page.open()

        # Attempt login with wrong password
        login_page.login(standard_user["username"], "wrong_password")

        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_message = login_page.get_error_message()
        assert error_message == TestData.INVALID_CREDENTIALS_ERROR, \
            f"Unexpected error message: {error_message}"

    @pytest.mark.auth
    @pytest.mark.negative
    @allure.title("Login with empty username")
    @allure.description("Verify error message when username is empty")
    def test_login_empty_username(self, login_page):
        """Test login with empty username."""
        # Navigate to login page
        login_page.open()

        # Attempt login with empty username
        login_page.login("", "secret_sauce")

        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_message = login_page.get_error_message()
        assert error_message == TestData.USERNAME_REQUIRED_ERROR, \
            f"Expected error: {TestData.USERNAME_REQUIRED_ERROR}, Got: {error_message}"

    @pytest.mark.auth
    @pytest.mark.negative
    @allure.title("Login with empty password")
    @allure.description("Verify error message when password is empty")
    def test_login_empty_password(self, login_page):
        """Test login with empty password."""
        # Navigate to login page
        login_page.open()

        # Attempt login with empty password
        login_page.login("standard_user", "")

        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_message = login_page.get_error_message()
        assert error_message == TestData.PASSWORD_REQUIRED_ERROR, \
            f"Expected error: {TestData.PASSWORD_REQUIRED_ERROR}, Got: {error_message}"

    @pytest.mark.auth
    @pytest.mark.negative
    @allure.title("Login with empty credentials")
    @allure.description("Verify error message when both username and password are empty")
    def test_login_empty_credentials(self, login_page):
        """Test login with both fields empty."""
        # Navigate to login page
        login_page.open()

        # Attempt login with empty credentials
        login_page.login("", "")

        # Verify error message (username error shown first)
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_message = login_page.get_error_message()
        assert error_message == TestData.USERNAME_REQUIRED_ERROR, \
            f"Expected error: {TestData.USERNAME_REQUIRED_ERROR}, Got: {error_message}"

    @pytest.mark.auth
    @pytest.mark.negative
    @allure.title("Error message can be closed")
    @allure.description("Verify error message can be dismissed")
    def test_close_error_message(self, login_page):
        """Test that error message can be closed."""
        # Navigate to login page
        login_page.open()

        # Trigger error
        login_page.login("", "")
        assert login_page.is_error_displayed(), "Error message not displayed"

        # Close error message
        login_page.close_error_message()

        # Verify error message is hidden
        assert not login_page.is_error_displayed(), "Error message still visible after closing"

    @pytest.mark.auth
    @pytest.mark.negative
    @allure.title("Login with special characters")
    @allure.description("Verify login fails gracefully with special characters")
    def test_login_special_characters(self, login_page):
        """Test login with special characters in credentials."""
        # Navigate to login page
        login_page.open()

        # Test various special characters
        special_chars = ["!@#$%", "'; DROP TABLE users;--", "<script>alert('xss')</script>", "../../etc/passwd"]

        for chars in special_chars:
            # Clear previous attempts
            login_page.clear_credentials()

            # Attempt login
            login_page.login(chars, chars)

            # Verify error handling
            assert login_page.is_error_displayed() or login_page.is_at_login_page(), \
                f"Unexpected behavior with special characters: {chars}"

            # Close error if displayed
            if login_page.is_error_displayed():
                login_page.close_error_message()

    @pytest.mark.auth
    @pytest.mark.negative
    @allure.title("Login with very long credentials")
    @allure.description("Verify login handles very long input gracefully")
    def test_login_long_credentials(self, login_page):
        """Test login with very long username and password."""
        # Navigate to login page
        login_page.open()

        # Create very long strings
        long_username = "a" * 1000
        long_password = "b" * 1000

        # Attempt login
        login_page.login(long_username, long_password)

        # Verify appropriate error handling
        assert login_page.is_error_displayed() or login_page.is_at_login_page(), \
            "Unexpected behavior with very long credentials"

        # Verify specific error if displayed
        if login_page.is_error_displayed():
            error_message = login_page.get_error_message()
            assert TestData.INVALID_CREDENTIALS_ERROR in error_message or \
                   TestData.USERNAME_REQUIRED_ERROR in error_message, \
                   f"Unexpected error message: {error_message}"

    @pytest.mark.auth
    @pytest.mark.negative
    @allure.title("Login case sensitivity")
    @allure.description("Verify login is case sensitive")
    def test_login_case_sensitivity(self, login_page):
        """Test that login is case sensitive."""
        # Navigate to login page
        login_page.open()

        # Try uppercase username
        login_page.login("STANDARD_USER", "secret_sauce")
        assert login_page.is_error_displayed(), "Login should be case sensitive for username"
        login_page.close_error_message()

        # Try uppercase password
        login_page.clear_credentials()
        login_page.login("standard_user", "SECRET_SAUCE")
        assert login_page.is_error_displayed(), "Login should be case sensitive for password"