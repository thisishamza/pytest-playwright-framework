"""
Add to cart test cases.
Tests adding products to cart from inventory and product detail pages.
"""

import pytest
import allure
from playwright.sync_api import expect


@allure.feature("Cart Management")
@allure.story("Add to Cart")
class TestAddToCart:
    """Add to cart functionality test cases."""

    @pytest.mark.cart
    @pytest.mark.positive
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("Add single product to cart")
    @allure.description("Verify single product can be added to cart from inventory")
    def test_add_single_product_to_cart(self, login_and_go_to_inventory):
        """Test adding a single product to cart."""
        inventory_page = login_and_go_to_inventory

        # Verify cart is empty initially
        assert inventory_page.get_cart_count() == 0, "Cart should be empty initially"

        # Add first product to cart
        product_name = inventory_page.get_product_name(0)
        inventory_page.add_product_to_cart_by_index(0)

        # Verify cart badge shows 1
        assert inventory_page.get_cart_count() == 1, "Cart should have 1 item"

        # Verify button changed to Remove
        assert inventory_page.is_product_added_to_cart(product_name), \
            "Product not marked as added to cart"

    @pytest.mark.cart
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Add multiple products to cart")
    @allure.description("Verify multiple products can be added to cart")
    def test_add_multiple_products_to_cart(self, login_and_go_to_inventory):
        """Test adding multiple products to cart."""
        inventory_page = login_and_go_to_inventory

        # Add 3 products to cart
        products_to_add = 3
        added_products = []

        for i in range(products_to_add):
            product_name = inventory_page.get_product_name(i)
            inventory_page.add_product_to_cart_by_index(i)
            added_products.append(product_name)

        # Verify cart count
        assert inventory_page.get_cart_count() == products_to_add, \
            f"Cart should have {products_to_add} items"

        # Verify all products show as added
        for product_name in added_products:
            assert inventory_page.is_product_added_to_cart(product_name), \
                f"Product {product_name} not marked as added"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Add all products to cart")
    @allure.description("Verify all products can be added to cart")
    def test_add_all_products_to_cart(self, login_and_go_to_inventory):
        """Test adding all products to cart."""
        inventory_page = login_and_go_to_inventory

        # Get total product count
        total_products = inventory_page.get_product_count()

        # Add all products
        inventory_page.add_all_products_to_cart()

        # Verify cart count
        assert inventory_page.get_cart_count() == total_products, \
            f"Cart should have {total_products} items"

        # Verify all products show Remove button
        products_in_cart = inventory_page.get_products_in_cart()
        assert len(products_in_cart) == total_products, \
            "Not all products marked as in cart"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Add product from detail page")
    @allure.description("Verify product can be added from product detail page")
    def test_add_product_from_detail_page(self, login_and_go_to_inventory, product_detail_page):
        """Test adding product from detail page."""
        inventory_page = login_and_go_to_inventory

        # Navigate to product detail
        product_name = inventory_page.get_product_name(0)
        inventory_page.click_product_name(product_name)

        # Verify on detail page
        assert product_detail_page.get_product_name() == product_name

        # Add to cart from detail page
        product_detail_page.add_to_cart()

        # Verify cart updated
        assert product_detail_page.get_cart_count() == 1, "Cart should have 1 item"
        assert product_detail_page.is_added_to_cart(), "Product not marked as added"

        # Return to inventory and verify
        product_detail_page.go_back_to_products()
        assert inventory_page.is_product_added_to_cart(product_name), \
            "Product not showing as added on inventory page"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Cart badge appears and updates")
    @allure.description("Verify cart badge appears when items added and updates count")
    def test_cart_badge_updates(self, login_and_go_to_inventory, header_component):
        """Test cart badge appearance and updates."""
        inventory_page = login_and_go_to_inventory

        # Initially no badge
        assert not header_component.is_cart_badge_visible(), \
            "Cart badge should not be visible when empty"

        # Add first item - badge appears
        inventory_page.add_product_to_cart_by_index(0)
        assert header_component.is_cart_badge_visible(), \
            "Cart badge should appear when item added"
        assert header_component.get_cart_count() == 1, "Badge should show 1"

        # Add second item - badge updates
        inventory_page.add_product_to_cart_by_index(1)
        assert header_component.get_cart_count() == 2, "Badge should show 2"

        # Add third item - badge updates
        inventory_page.add_product_to_cart_by_index(2)
        assert header_component.get_cart_count() == 3, "Badge should show 3"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Add product by name")
    @allure.description("Verify specific product can be added by name")
    def test_add_specific_product_by_name(self, login_and_go_to_inventory):
        """Test adding specific product by name."""
        inventory_page = login_and_go_to_inventory

        # Add specific product
        target_product = "Sauce Labs Bolt T-Shirt"
        inventory_page.add_product_to_cart(target_product)

        # Verify added
        assert inventory_page.is_product_added_to_cart(target_product), \
            f"{target_product} not added to cart"
        assert inventory_page.get_cart_count() == 1, "Cart count incorrect"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Add to cart button state change")
    @allure.description("Verify Add to cart button changes to Remove after adding")
    def test_add_to_cart_button_state(self, login_and_go_to_inventory, product_card_factory):
        """Test button state changes when adding to cart."""
        inventory_page = login_and_go_to_inventory

        # Get first product card
        card = product_card_factory.get_product_card_by_index(0)

        # Initially shows Add to cart
        assert card.get_button_text() == "Add to cart", \
            "Initial button text should be 'Add to cart'"
        assert not card.is_in_cart(), "Product should not be in cart initially"

        # Add to cart
        card.add_to_cart()

        # Button changes to Remove
        assert card.get_button_text() == "Remove", \
            "Button text should change to 'Remove'"
        assert card.is_in_cart(), "Product should be marked as in cart"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Add products with different users")
    @allure.description("Verify add to cart works for different user types")
    def test_add_to_cart_different_users(self, page, login_page, inventory_page, users_that_can_login):
        """Test add to cart functionality with different users."""
        # Login with parametrized user
        login_page.open()
        login_page.login(users_that_can_login["username"], users_that_can_login["password"])

        # Wait for inventory page
        timeout = 10000 if "performance" in users_that_can_login["username"] else 5000
        inventory_page.wait.wait_for_element(".inventory_list", timeout=timeout)

        # Add product to cart
        inventory_page.add_product_to_cart_by_index(0)

        # Verify cart updated (may have issues for problem_user)
        cart_count = inventory_page.get_cart_count()
        if users_that_can_login["expected_behavior"] != "buggy":
            assert cart_count == 1, f"Cart not updated for {users_that_can_login['username']}"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Verify cart persistence across pages")
    @allure.description("Verify cart items persist when navigating between pages")
    def test_cart_persistence_across_pages(self, login_and_go_to_inventory, cart_page):
        """Test that cart items persist across page navigation."""
        inventory_page = login_and_go_to_inventory

        # Add items to cart
        products_added = []
        for i in range(2):
            name = inventory_page.get_product_name(i)
            inventory_page.add_product_to_cart_by_index(i)
            products_added.append(name)

        # Navigate to cart
        inventory_page.go_to_cart()

        # Verify items in cart
        cart_items = cart_page.get_all_cart_item_names()
        for product in products_added:
            assert product in cart_items, f"{product} not found in cart"

        # Return to inventory
        cart_page.continue_shopping()

        # Verify items still marked as in cart
        for product in products_added:
            assert inventory_page.is_product_added_to_cart(product), \
                f"{product} not marked as in cart after navigation"