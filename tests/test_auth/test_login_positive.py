"""
Positive login test cases for Saucedemo application.
Tests successful login scenarios with different user types.
"""

import pytest
import allure
from playwright.sync_api import expect
from config.test_users import TestUsers
from data.test_data import TestData


@allure.feature("Authentication")
@allure.story("Login - Positive Cases")
class TestLoginPositive:
    """Positive login test cases."""

    @pytest.mark.smoke
    @pytest.mark.auth
    @pytest.mark.positive
    @allure.title("Login with standard user")
    @allure.description("Verify successful login with standard_user credentials")
    def test_login_standard_user(self, login_page, inventory_page, standard_user):
        """Test successful login with standard user."""
        # Navigate to login page
        login_page.open()

        # Verify login page is displayed
        assert login_page.is_at_login_page(), "Login page is not displayed"

        # Perform login
        login_page.login(standard_user["username"], standard_user["password"])

        # Verify successful login
        assert login_page.verify_login_successful(), "Login was not successful"

        # Verify inventory page is displayed
        expect(inventory_page.inventory_list).to_be_visible()
        assert inventory_page.get_product_count() == 6, "Expected 6 products on inventory page"

    @pytest.mark.auth
    @pytest.mark.positive
    @pytest.mark.slow
    @allure.title("Login with performance glitch user")
    @allure.description("Verify login with performance_glitch_user (slow performance)")
    def test_login_performance_glitch_user(self, login_page, inventory_page, performance_glitch_user):
        """Test login with performance glitch user."""
        # Navigate to login page
        login_page.open()

        # Perform login
        login_page.login(
            performance_glitch_user["username"],
            performance_glitch_user["password"]
        )

        # Wait longer for slow performance user
        inventory_page.wait.wait_for_element(".inventory_list", timeout=10000)

        # Verify successful login despite slow performance
        assert inventory_page.inventory_list.is_visible(), "Inventory page not loaded"
        assert inventory_page.get_product_count() == 6, "Products not loaded correctly"

    @pytest.mark.auth
    @pytest.mark.positive
    @allure.title("Login with problem user")
    @allure.description("Verify login with problem_user (has checkout issues)")
    def test_login_problem_user(self, login_page, inventory_page, problem_user):
        """Test login with problem user."""
        # Navigate to login page
        login_page.open()

        # Perform login
        login_page.login(problem_user["username"], problem_user["password"])

        # Verify successful login (user can login but has issues later)
        assert login_page.verify_login_successful(), "Login was not successful"
        expect(inventory_page.inventory_list).to_be_visible()

    @pytest.mark.auth
    @pytest.mark.positive
    @allure.title("Login with error user")
    @allure.description("Verify login with error_user (triggers application errors)")
    def test_login_error_user(self, login_page, inventory_page, error_user):
        """Test login with error user."""
        # Navigate to login page
        login_page.open()

        # Perform login
        login_page.login(error_user["username"], error_user["password"])

        # Verify successful login (user can login but causes errors later)
        assert login_page.verify_login_successful(), "Login was not successful"
        expect(inventory_page.inventory_list).to_be_visible()

    @pytest.mark.auth
    @pytest.mark.positive
    @allure.title("Login with visual user")
    @allure.description("Verify login with visual_user (has visual inconsistencies)")
    def test_login_visual_user(self, login_page, inventory_page, visual_user):
        """Test login with visual user."""
        # Navigate to login page
        login_page.open()

        # Perform login
        login_page.login(visual_user["username"], visual_user["password"])

        # Verify successful login (user can login but has visual issues)
        assert login_page.verify_login_successful(), "Login was not successful"
        expect(inventory_page.inventory_list).to_be_visible()

    @pytest.mark.auth
    @pytest.mark.positive
    @allure.title("Login with all valid users")
    @allure.description("Verify login works for all users that can login")
    def test_login_all_valid_users(self, login_page, inventory_page, users_that_can_login):
        """Test login with all users that should be able to login."""
        # Navigate to login page
        login_page.open()

        # Get user credentials
        username = users_that_can_login["username"]
        password = users_that_can_login["password"]

        # Perform login
        login_page.login(username, password)

        # Set appropriate timeout based on user type
        timeout = 10000 if "performance" in username else 5000

        # Wait for navigation
        inventory_page.wait.wait_for_element(".inventory_list", timeout=timeout)

        # Verify successful login
        assert inventory_page.inventory_list.is_visible(), f"Login failed for user: {username}"

        # Log success
        allure.attach(
            f"Successfully logged in with user: {username}",
            name="Login Success",
            attachment_type=allure.attachment_type.TEXT
        )

    @pytest.mark.auth
    @pytest.mark.positive
    @pytest.mark.smoke
    @allure.title("Login with Enter key")
    @allure.description("Verify login works by pressing Enter key instead of clicking button")
    def test_login_with_enter_key(self, login_page, inventory_page, standard_user):
        """Test login using Enter key instead of clicking login button."""
        # Navigate to login page
        login_page.open()

        # Enter credentials and press Enter
        login_page.login_with_enter_key(
            standard_user["username"],
            standard_user["password"]
        )

        # Verify successful login
        assert login_page.verify_login_successful(), "Login with Enter key failed"
        expect(inventory_page.inventory_list).to_be_visible()

    @pytest.mark.auth
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Login state persistence")
    @allure.description("Verify user remains logged in when navigating between pages")
    def test_login_state_persistence(self, login_page, inventory_page, cart_page, standard_user):
        """Test that login state persists across page navigation."""
        # Login
        login_page.open()
        login_page.login(standard_user["username"], standard_user["password"])

        # Navigate to cart
        inventory_page.go_to_cart()
        assert cart_page.page_title.is_visible(), "Cart page not accessible"

        # Go back to inventory
        cart_page.continue_shopping()
        assert inventory_page.inventory_list.is_visible(), "Lost login state"

        # Verify still logged in
        assert not login_page.is_at_login_page(), "Unexpectedly returned to login page"