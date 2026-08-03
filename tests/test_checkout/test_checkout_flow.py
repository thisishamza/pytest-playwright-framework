"""
Complete checkout flow test cases.
Tests the entire checkout process from cart to order confirmation.
"""

import pytest
import allure
from data.test_data import TestData


@allure.feature("Checkout")
@allure.story("Checkout Flow")
class TestCheckoutFlow:
    """Complete checkout flow test cases."""

    @pytest.mark.checkout
    @pytest.mark.e2e
    @pytest.mark.positive
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("Complete checkout with single item")
    @allure.description("Verify complete checkout flow with one product")
    def test_checkout_single_item(
        self,
        login_and_go_to_inventory,
        cart_page,
        checkout_info_page,
        checkout_overview_page,
        checkout_complete_page,
        valid_checkout_data
    ):
        """Test complete checkout flow with single item."""
        inventory_page = login_and_go_to_inventory

        # Add single product to cart
        product_name = inventory_page.get_product_name(0)
        product_price = inventory_page.get_product_price(0)
        inventory_page.add_product_to_cart_by_index(0)

        # Go to cart
        inventory_page.go_to_cart()
        assert cart_page.is_item_in_cart(product_name), "Product not in cart"

        # Proceed to checkout
        cart_page.proceed_to_checkout()

        # Fill checkout information
        checkout_info_page.fill_checkout_form(
            valid_checkout_data["first_name"],
            valid_checkout_data["last_name"],
            valid_checkout_data["postal_code"]
        )
        checkout_info_page.click_continue()

        # Verify checkout overview
        assert checkout_overview_page.get_cart_items_count() == 1, \
            "Wrong number of items in checkout"

        # Verify totals
        assert checkout_overview_page.verify_totals(), "Totals calculation incorrect"

        # Complete order
        checkout_overview_page.click_finish()

        # Verify order completion
        assert checkout_complete_page.is_order_complete(), "Order not completed"
        assert checkout_complete_page.verify_order_success(), "Order success not verified"

        # Verify cart is empty
        assert checkout_complete_page.verify_cart_is_empty(), "Cart not empty after order"

    @pytest.mark.checkout
    @pytest.mark.e2e
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Complete checkout with multiple items")
    @allure.description("Verify complete checkout flow with multiple products")
    def test_checkout_multiple_items(
        self,
        add_items_to_cart,
        cart_page,
        checkout_info_page,
        checkout_overview_page,
        checkout_complete_page,
        valid_checkout_data
    ):
        """Test complete checkout flow with multiple items."""
        inventory_page = add_items_to_cart

        # Go to cart
        inventory_page.go_to_cart()
        assert cart_page.get_cart_items_count() == 3, "Expected 3 items in cart"

        # Proceed to checkout
        cart_page.proceed_to_checkout()

        # Fill checkout information
        checkout_info_page.complete_step_with_valid_data(
            valid_checkout_data["first_name"],
            valid_checkout_data["last_name"],
            valid_checkout_data["postal_code"]
        )

        # Verify checkout overview
        assert checkout_overview_page.get_cart_items_count() == 3, \
            "Wrong number of items in checkout"

        # Verify payment and shipping info
        payment_info = checkout_overview_page.get_payment_information()
        assert payment_info, "Payment information missing"

        shipping_info = checkout_overview_page.get_shipping_information()
        assert shipping_info, "Shipping information missing"

        # Verify totals
        assert checkout_overview_page.verify_totals(), "Totals calculation incorrect"

        # Complete order
        checkout_overview_page.complete_order()

        # Verify order completion
        assert checkout_complete_page.verify_order_success(), "Order not successful"

    @pytest.mark.checkout
    @pytest.mark.positive
    @allure.title("Checkout with different valid users")
    @allure.description("Verify checkout works for users that can complete checkout")
    def test_checkout_different_users(
        self,
        page,
        login_page,
        inventory_page,
        cart_page,
        checkout_info_page,
        checkout_overview_page,
        checkout_complete_page,
        users_that_can_checkout,
        valid_checkout_data
    ):
        """Test checkout with different user types."""
        # Login with parametrized user
        login_page.open()
        login_page.login(
            users_that_can_checkout["username"],
            users_that_can_checkout["password"]
        )

        # Wait for inventory
        timeout = 10000 if "performance" in users_that_can_checkout["username"] else 5000
        inventory_page.wait.wait_for_element(".inventory_list", timeout=timeout)

        # Add product and checkout
        inventory_page.add_product_to_cart_by_index(0)
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        # Fill information
        checkout_info_page.complete_step_with_valid_data()

        # Complete order
        checkout_overview_page.click_finish()

        # Verify completion
        assert checkout_complete_page.is_order_complete(), \
            f"Checkout failed for {users_that_can_checkout['username']}"

    @pytest.mark.checkout
    @pytest.mark.negative
    @allure.title("Checkout validation - empty first name")
    @allure.description("Verify checkout shows error for missing first name")
    def test_checkout_empty_first_name(
        self,
        add_items_to_cart,
        cart_page,
        checkout_info_page
    ):
        """Test checkout validation for empty first name."""
        inventory_page = add_items_to_cart

        # Go to checkout
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        # Submit with empty first name
        checkout_info_page.submit_form_missing_first_name("Doe", "12345")

        # Verify error
        assert checkout_info_page.is_error_displayed(), "Error not displayed"
        error = checkout_info_page.get_error_message()
        assert error == TestData.FIRST_NAME_REQUIRED_ERROR, \
            f"Wrong error: {error}"

    @pytest.mark.checkout
    @pytest.mark.negative
    @allure.title("Checkout validation - empty last name")
    @allure.description("Verify checkout shows error for missing last name")
    def test_checkout_empty_last_name(
        self,
        add_items_to_cart,
        cart_page,
        checkout_info_page
    ):
        """Test checkout validation for empty last name."""
        inventory_page = add_items_to_cart

        # Go to checkout
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        # Submit with empty last name
        checkout_info_page.submit_form_missing_last_name("John", "12345")

        # Verify error
        assert checkout_info_page.is_error_displayed(), "Error not displayed"
        error = checkout_info_page.get_error_message()
        assert error == TestData.LAST_NAME_REQUIRED_ERROR, \
            f"Wrong error: {error}"

    @pytest.mark.checkout
    @pytest.mark.negative
    @allure.title("Checkout validation - empty postal code")
    @allure.description("Verify checkout shows error for missing postal code")
    def test_checkout_empty_postal_code(
        self,
        add_items_to_cart,
        cart_page,
        checkout_info_page
    ):
        """Test checkout validation for empty postal code."""
        inventory_page = add_items_to_cart

        # Go to checkout
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()

        # Submit with empty postal code
        checkout_info_page.submit_form_missing_postal_code("John", "Doe")

        # Verify error
        assert checkout_info_page.is_error_displayed(), "Error not displayed"
        error = checkout_info_page.get_error_message()
        assert error == TestData.POSTAL_CODE_REQUIRED_ERROR, \
            f"Wrong error: {error}"

    @pytest.mark.checkout
    @pytest.mark.positive
    @allure.title("Cancel checkout at info step")
    @allure.description("Verify cancel button returns to cart from checkout info")
    def test_cancel_checkout_at_info(
        self,
        add_items_to_cart,
        cart_page,
        checkout_info_page
    ):
        """Test canceling checkout at information step."""
        inventory_page = add_items_to_cart

        # Go to checkout
        inventory_page.go_to_cart()
        initial_cart_count = cart_page.get_cart_items_count()
        cart_page.proceed_to_checkout()

        # Cancel checkout
        checkout_info_page.cancel_checkout()

        # Verify returned to cart
        assert cart_page.page_title.is_visible(), "Not returned to cart"
        assert cart_page.get_cart_items_count() == initial_cart_count, \
            "Cart items changed"

    @pytest.mark.checkout
    @pytest.mark.positive
    @allure.title("Cancel checkout at overview step")
    @allure.description("Verify cancel button works from checkout overview")
    def test_cancel_checkout_at_overview(
        self,
        add_items_to_cart,
        cart_page,
        checkout_info_page,
        checkout_overview_page,
        inventory_page
    ):
        """Test canceling checkout at overview step."""
        inv_page = add_items_to_cart

        # Go through checkout to overview
        inv_page.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_info_page.complete_step_with_valid_data()

        # Cancel from overview
        checkout_overview_page.cancel_order()

        # Verify returned to inventory
        assert inventory_page.inventory_list.is_visible(), \
            "Not returned to inventory"

        # Verify items still in cart
        assert inventory_page.get_cart_count() == 3, "Cart items lost"

    @pytest.mark.checkout
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Return home after order completion")
    @allure.description("Verify Back Home button returns to inventory after order")
    def test_return_home_after_order(
        self,
        add_items_to_cart,
        cart_page,
        checkout_info_page,
        checkout_overview_page,
        checkout_complete_page,
        inventory_page
    ):
        """Test returning to inventory after completing order."""
        inv_page = add_items_to_cart

        # Complete checkout
        inv_page.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_info_page.complete_step_with_valid_data()
        checkout_overview_page.complete_order()

        # Verify order complete
        assert checkout_complete_page.is_order_complete()

        # Return home
        checkout_complete_page.go_back_to_products()

        # Verify on inventory page with empty cart
        assert inventory_page.inventory_list.is_visible(), "Not on inventory page"
        assert inventory_page.get_cart_count() == 0, "Cart not empty"

    @pytest.mark.checkout
    @pytest.mark.positive
    @allure.title("Price calculation verification")
    @allure.description("Verify subtotal, tax, and total calculations")
    def test_checkout_price_calculations(
        self,
        login_and_go_to_inventory,
        cart_page,
        checkout_info_page,
        checkout_overview_page
    ):
        """Test price calculations in checkout."""
        inventory_page = login_and_go_to_inventory

        # Add products with known prices
        prices = []
        for i in range(2):
            prices.append(inventory_page.get_product_price(i))
            inventory_page.add_product_to_cart_by_index(i)

        expected_subtotal = sum(prices)
        expected_tax = TestData.calculate_tax(expected_subtotal)
        expected_total = TestData.calculate_total(expected_subtotal)

        # Go through checkout
        inventory_page.go_to_cart()
        cart_page.proceed_to_checkout()
        checkout_info_page.complete_step_with_valid_data()

        # Verify calculations
        actual_subtotal = checkout_overview_page.get_subtotal()
        actual_tax = checkout_overview_page.get_tax()
        actual_total = checkout_overview_page.get_total()

        assert abs(actual_subtotal - expected_subtotal) < 0.01, \
            f"Subtotal mismatch: {actual_subtotal} vs {expected_subtotal}"
        assert abs(actual_tax - expected_tax) < 0.01, \
            f"Tax mismatch: {actual_tax} vs {expected_tax}"
        assert abs(actual_total - expected_total) < 0.01, \
            f"Total mismatch: {actual_total} vs {expected_total}"