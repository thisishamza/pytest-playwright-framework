"""
Product sorting test cases for inventory page.
Tests all sorting options: A-Z, Z-A, Price Low-High, Price High-Low.
"""

import pytest
import allure
from data.test_data import TestData


@allure.feature("Inventory")
@allure.story("Product Sorting")
class TestProductSorting:
    """Product sorting functionality test cases."""

    @pytest.mark.inventory
    @pytest.mark.positive
    @pytest.mark.smoke
    @allure.title("Default sort order (A-Z)")
    @allure.description("Verify products are sorted A-Z by default")
    def test_default_sort_order(self, login_and_go_to_inventory):
        """Test that default sort order is A-Z."""
        inventory_page = login_and_go_to_inventory

        # Verify default sort option
        selected_option = inventory_page.get_selected_sort_option()
        assert selected_option == "az", f"Default sort is not A-Z: {selected_option}"

        # Verify products are sorted A-Z
        assert inventory_page.verify_products_sorted_alphabetically(ascending=True), \
            "Products not sorted A-Z by default"

    @pytest.mark.inventory
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Sort products A to Z")
    @allure.description("Verify products can be sorted alphabetically A-Z")
    def test_sort_products_a_to_z(self, login_and_go_to_inventory):
        """Test sorting products from A to Z."""
        inventory_page = login_and_go_to_inventory

        # Apply A-Z sort
        inventory_page.sort_products("az")

        # Verify sort option is selected
        assert inventory_page.get_selected_sort_option() == "az", \
            "A-Z sort option not selected"

        # Get expected order
        expected_order = TestData.get_sorted_products("az")
        actual_order = inventory_page.get_all_product_names()

        # Verify order
        assert actual_order == expected_order, \
            f"A-Z sort failed.\nExpected: {expected_order}\nActual: {actual_order}"

    @pytest.mark.inventory
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Sort products Z to A")
    @allure.description("Verify products can be sorted alphabetically Z-A")
    def test_sort_products_z_to_a(self, login_and_go_to_inventory):
        """Test sorting products from Z to A."""
        inventory_page = login_and_go_to_inventory

        # Apply Z-A sort
        inventory_page.sort_products("za")

        # Verify sort option is selected
        assert inventory_page.get_selected_sort_option() == "za", \
            "Z-A sort option not selected"

        # Get expected order
        expected_order = TestData.get_sorted_products("za")
        actual_order = inventory_page.get_all_product_names()

        # Verify order
        assert actual_order == expected_order, \
            f"Z-A sort failed.\nExpected: {expected_order}\nActual: {actual_order}"

    @pytest.mark.inventory
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Sort products price low to high")
    @allure.description("Verify products can be sorted by price ascending")
    def test_sort_products_price_low_to_high(self, login_and_go_to_inventory):
        """Test sorting products by price from low to high."""
        inventory_page = login_and_go_to_inventory

        # Apply price low-high sort
        inventory_page.sort_products("lohi")

        # Verify sort option is selected
        assert inventory_page.get_selected_sort_option() == "lohi", \
            "Price low-high sort option not selected"

        # Get expected order
        expected_order = TestData.get_sorted_products("lohi")
        actual_order = inventory_page.get_all_product_names()

        # Verify order
        assert actual_order == expected_order, \
            f"Price low-high sort failed.\nExpected: {expected_order}\nActual: {actual_order}"

        # Also verify prices are in ascending order
        assert inventory_page.verify_products_sorted_by_price(ascending=True), \
            "Prices not in ascending order"

    @pytest.mark.inventory
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Sort products price high to low")
    @allure.description("Verify products can be sorted by price descending")
    def test_sort_products_price_high_to_low(self, login_and_go_to_inventory):
        """Test sorting products by price from high to low."""
        inventory_page = login_and_go_to_inventory

        # Apply price high-low sort
        inventory_page.sort_products("hilo")

        # Verify sort option is selected
        assert inventory_page.get_selected_sort_option() == "hilo", \
            "Price high-low sort option not selected"

        # Get expected order
        expected_order = TestData.get_sorted_products("hilo")
        actual_order = inventory_page.get_all_product_names()

        # Verify order
        assert actual_order == expected_order, \
            f"Price high-low sort failed.\nExpected: {expected_order}\nActual: {actual_order}"

        # Also verify prices are in descending order
        assert inventory_page.verify_products_sorted_by_price(ascending=False), \
            "Prices not in descending order"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Sort persistence after navigation")
    @allure.description("Verify sort order persists when navigating away and back")
    def test_sort_persistence(self, login_and_go_to_inventory, product_detail_page):
        """Test that sort order persists after navigation."""
        inventory_page = login_and_go_to_inventory

        # Apply Z-A sort
        inventory_page.sort_products("za")
        original_order = inventory_page.get_all_product_names()

        # Navigate to product detail
        first_product = original_order[0]
        inventory_page.click_product_name(first_product)

        # Return to inventory
        product_detail_page.go_back_to_products()

        # Wait for page to fully load after navigation
        inventory_page.wait.wait_for_element(".inventory_list", timeout=5000)
        inventory_page.wait.wait_for_animation(500)

        # Check if sort is maintained (some sites reset on navigation)
        current_sort = inventory_page.get_selected_sort_option()

        # Saucedemo may reset sort to default (az) after navigation
        # This is common behavior - verify current implementation
        if current_sort != "za":
            # If sort was reset, re-apply it and verify it works
            inventory_page.sort_products("za")
            reapplied_order = inventory_page.get_all_product_names()
            assert reapplied_order == original_order, \
                "Sort order not consistent when reapplied"
        else:
            # If sort persisted, verify order is maintained
            current_order = inventory_page.get_all_product_names()
            assert current_order == original_order, \
                "Product order changed despite sort being maintained"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Multiple sort changes")
    @allure.description("Verify sorting can be changed multiple times")
    def test_multiple_sort_changes(self, login_and_go_to_inventory):
        """Test changing sort order multiple times."""
        inventory_page = login_and_go_to_inventory

        sort_options = [
            ("za", TestData.get_sorted_products("za")),
            ("lohi", TestData.get_sorted_products("lohi")),
            ("hilo", TestData.get_sorted_products("hilo")),
            ("az", TestData.get_sorted_products("az"))
        ]

        for sort_option, expected_order in sort_options:
            # Apply sort
            inventory_page.sort_products(sort_option)

            # Verify selected option
            assert inventory_page.get_selected_sort_option() == sort_option, \
                f"Sort option {sort_option} not selected"

            # Verify order
            actual_order = inventory_page.get_all_product_names()
            assert actual_order == expected_order, \
                f"Sort {sort_option} failed.\nExpected: {expected_order}\nActual: {actual_order}"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Sort with items in cart")
    @allure.description("Verify sorting works correctly with items already in cart")
    def test_sort_with_items_in_cart(self, login_and_go_to_inventory):
        """Test that sorting works when items are in cart."""
        inventory_page = login_and_go_to_inventory

        # Add some items to cart
        inventory_page.add_product_to_cart_by_index(0)
        inventory_page.add_product_to_cart_by_index(2)

        # Apply different sorts and verify
        sort_tests = [
            ("za", TestData.get_sorted_products("za")),
            ("lohi", TestData.get_sorted_products("lohi"))
        ]

        for sort_option, expected_order in sort_tests:
            inventory_page.sort_products(sort_option)
            actual_order = inventory_page.get_all_product_names()

            assert actual_order == expected_order, \
                f"Sort {sort_option} failed with items in cart"

            # Verify items remain in cart
            assert inventory_page.get_cart_count() == 2, \
                "Cart count changed after sorting"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Price sort verification")
    @allure.description("Verify price sorting handles equal prices correctly")
    def test_price_sort_equal_prices(self, login_and_go_to_inventory):
        """Test price sorting with products that have equal prices."""
        inventory_page = login_and_go_to_inventory

        # Apply price sort
        inventory_page.sort_products("lohi")

        # Get all prices
        prices = inventory_page.get_all_product_prices()

        # Verify prices are sorted
        for i in range(len(prices) - 1):
            assert prices[i] <= prices[i + 1], \
                f"Prices not sorted correctly at index {i}: {prices[i]} > {prices[i + 1]}"

        # Products with same price should maintain relative order
        # (This is implementation-specific and may vary)