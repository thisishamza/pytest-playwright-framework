"""
Remove from cart test cases.
Tests removing products from cart from inventory and cart pages.
"""

import pytest
import allure


@allure.feature("Cart Management")
@allure.story("Remove from Cart")
class TestRemoveFromCart:
    """Remove from cart functionality test cases."""

    @pytest.mark.cart
    @pytest.mark.positive
    @pytest.mark.smoke
    @allure.title("Remove single product from inventory page")
    @allure.description("Verify product can be removed from cart on inventory page")
    def test_remove_single_product_from_inventory(self, login_and_go_to_inventory):
        """Test removing single product from cart on inventory page."""
        inventory_page = login_and_go_to_inventory

        # Add product to cart
        product_name = inventory_page.get_product_name(0)
        inventory_page.add_product_to_cart_by_index(0)
        assert inventory_page.get_cart_count() == 1, "Product not added"

        # Remove product from cart
        inventory_page.remove_product_from_cart(product_name)

        # Verify cart is empty
        assert inventory_page.get_cart_count() == 0, "Cart should be empty"
        assert not inventory_page.is_product_added_to_cart(product_name), \
            "Product still marked as in cart"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Remove multiple products from inventory page")
    @allure.description("Verify multiple products can be removed from cart")
    def test_remove_multiple_products_from_inventory(self, login_and_go_to_inventory):
        """Test removing multiple products from cart."""
        inventory_page = login_and_go_to_inventory

        # Add 3 products
        products = []
        for i in range(3):
            name = inventory_page.get_product_name(i)
            inventory_page.add_product_to_cart_by_index(i)
            products.append(name)

        assert inventory_page.get_cart_count() == 3, "Products not added"

        # Remove products one by one
        for i, product in enumerate(products):
            inventory_page.remove_product_from_cart(product)
            expected_count = 3 - (i + 1)
            assert inventory_page.get_cart_count() == expected_count, \
                f"Cart should have {expected_count} items"

        # Verify all removed
        for product in products:
            assert not inventory_page.is_product_added_to_cart(product), \
                f"{product} still marked as in cart"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Remove product from cart page")
    @allure.description("Verify product can be removed from cart page")
    def test_remove_product_from_cart_page(self, login_and_go_to_inventory, cart_page):
        """Test removing product from cart page."""
        inventory_page = login_and_go_to_inventory

        # Add products to cart
        products = []
        for i in range(2):
            name = inventory_page.get_product_name(i)
            inventory_page.add_product_to_cart_by_index(i)
            products.append(name)

        # Go to cart
        inventory_page.go_to_cart()

        # Remove first product
        cart_page.remove_item_from_cart(products[0])

        # Verify removed
        assert cart_page.get_cart_items_count() == 1, "Product not removed"
        assert not cart_page.is_item_in_cart(products[0]), \
            f"{products[0]} still in cart"
        assert cart_page.is_item_in_cart(products[1]), \
            f"{products[1]} should still be in cart"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Remove all products from cart page")
    @allure.description("Verify all products can be removed from cart")
    def test_remove_all_products_from_cart_page(self, add_items_to_cart, cart_page):
        """Test removing all products from cart page."""
        inventory_page = add_items_to_cart

        # Go to cart
        inventory_page.go_to_cart()

        # Verify items in cart
        initial_count = cart_page.get_cart_items_count()
        assert initial_count == 3, "Expected 3 items in cart"

        # Remove all items
        cart_page.remove_all_items_from_cart()

        # Verify cart is empty
        assert cart_page.is_cart_empty(), "Cart should be empty"
        assert cart_page.get_cart_items_count() == 0, "Cart still has items"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Remove product from detail page")
    @allure.description("Verify product can be removed from product detail page")
    def test_remove_product_from_detail_page(self, login_and_go_to_inventory, product_detail_page):
        """Test removing product from detail page."""
        inventory_page = login_and_go_to_inventory

        # Add product to cart
        product_name = inventory_page.get_product_name(0)
        inventory_page.add_product_to_cart_by_index(0)

        # Navigate to product detail
        inventory_page.click_product_name(product_name)

        # Verify product is in cart
        assert product_detail_page.is_added_to_cart(), "Product not in cart"

        # Remove from cart
        product_detail_page.remove_from_cart()

        # Verify removed
        assert not product_detail_page.is_added_to_cart(), "Product still in cart"
        assert product_detail_page.get_cart_count() == 0, "Cart should be empty"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Cart badge disappears when empty")
    @allure.description("Verify cart badge disappears when all items removed")
    def test_cart_badge_disappears(self, login_and_go_to_inventory, header_component):
        """Test that cart badge disappears when cart is empty."""
        inventory_page = login_and_go_to_inventory

        # Add and remove item
        inventory_page.add_product_to_cart_by_index(0)
        assert header_component.is_cart_badge_visible(), "Badge should appear"

        inventory_page.remove_product_from_cart_by_index(0)
        assert not header_component.is_cart_badge_visible(), \
            "Badge should disappear when cart empty"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Remove specific product keeps others")
    @allure.description("Verify removing one product doesn't affect others")
    def test_remove_specific_product(self, add_items_to_cart, cart_page):
        """Test that removing one product keeps others in cart."""
        inventory_page = add_items_to_cart

        # Get product names
        products = []
        for i in range(3):
            products.append(inventory_page.get_product_name(i))

        # Go to cart
        inventory_page.go_to_cart()

        # Remove middle product
        cart_page.remove_item_from_cart(products[1])

        # Verify correct products remain
        remaining_items = cart_page.get_all_cart_item_names()
        assert len(remaining_items) == 2, "Should have 2 items remaining"
        assert products[0] in remaining_items, f"{products[0]} should remain"
        assert products[2] in remaining_items, f"{products[2]} should remain"
        assert products[1] not in remaining_items, f"{products[1]} should be removed"

    @pytest.mark.cart
    @pytest.mark.positive
    @allure.title("Button state changes after removal")
    @allure.description("Verify Remove button changes back to Add to cart")
    def test_button_state_after_removal(self, login_and_go_to_inventory, product_card_factory):
        """Test button state changes after removing from cart."""
        inventory_page = login_and_go_to_inventory

        # Get product card
        card = product_card_factory.get_product_card_by_index(0)

        # Add to cart
        card.add_to_cart()
        assert card.get_button_text() == "Remove", "Button should show Remove"

        # Remove from cart
        card.remove_from_cart()
        assert card.get_button_text() == "Add to cart", \
            "Button should change back to Add to cart"
        assert not card.is_in_cart(), "Product should not be in cart"

    @pytest.mark.cart
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Remove and re-add product")
    @allure.description("Verify product can be removed and added again")
    def test_remove_and_readd_product(self, login_and_go_to_inventory):
        """Test removing and re-adding the same product."""
        inventory_page = login_and_go_to_inventory

        product_name = inventory_page.get_product_name(0)

        # Add product
        inventory_page.add_product_to_cart(product_name)
        assert inventory_page.get_cart_count() == 1, "Product not added"

        # Remove product
        inventory_page.remove_product_from_cart(product_name)
        assert inventory_page.get_cart_count() == 0, "Product not removed"

        # Add again
        inventory_page.add_product_to_cart(product_name)
        assert inventory_page.get_cart_count() == 1, "Product not re-added"
        assert inventory_page.is_product_added_to_cart(product_name), \
            "Product not marked as in cart"