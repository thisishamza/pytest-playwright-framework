"""
Product listing test cases for inventory page.
Tests product display, information, and basic interactions.
"""

import pytest
import allure
from playwright.sync_api import expect
from data.test_data import TestData


@allure.feature("Inventory")
@allure.story("Product Listing")
class TestProductListing:
    """Product listing and display test cases."""

    @pytest.mark.inventory
    @pytest.mark.smoke
    @pytest.mark.positive
    @allure.title("Display all products")
    @allure.description("Verify all 6 products are displayed on inventory page")
    def test_display_all_products(self, login_and_go_to_inventory):
        """Test that all products are displayed."""
        inventory_page = login_and_go_to_inventory

        # Verify product count
        product_count = inventory_page.get_product_count()
        assert product_count == 6, f"Expected 6 products, found {product_count}"

        # Verify inventory container is visible
        assert inventory_page.inventory_list.is_visible(), "Inventory list not visible"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Verify product information")
    @allure.description("Verify each product has name, description, price, and image")
    def test_product_information_complete(self, login_and_go_to_inventory):
        """Test that all products have complete information."""
        inventory_page = login_and_go_to_inventory
        products = TestData.get_product_list()

        for i in range(inventory_page.get_product_count()):
            # Get product information
            name = inventory_page.get_product_name(i)
            description = inventory_page.get_product_description(i)
            price = inventory_page.get_product_price(i)

            # Verify information is present
            assert name, f"Product {i} has no name"
            assert description, f"Product {i} has no description"
            assert price > 0, f"Product {i} has invalid price: {price}"

            # Verify product image is visible
            product = inventory_page.inventory_items.nth(i)
            images = product.locator("img")
            assert images.count() > 0, f"Product {i} has no image"
            image = images.first
            image.wait_for(state="attached", timeout=3000)
            assert image.get_attribute("src"), f"Product {i} image has no src"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Verify product names")
    @allure.description("Verify all expected products are present with correct names")
    def test_product_names(self, login_and_go_to_inventory):
        """Test that all expected products are present."""
        inventory_page = login_and_go_to_inventory
        expected_products = TestData.get_sorted_products("az")

        # Get actual product names
        actual_products = inventory_page.get_all_product_names()

        # Verify all expected products are present
        assert actual_products == expected_products, \
            f"Product names mismatch.\nExpected: {expected_products}\nActual: {actual_products}"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Verify product prices")
    @allure.description("Verify product prices match expected values")
    def test_product_prices(self, login_and_go_to_inventory):
        """Test that product prices are correct."""
        inventory_page = login_and_go_to_inventory
        products_data = TestData.get_product_list()

        # Create price map from test data
        expected_prices = {p["name"]: p["price"] for p in products_data}

        # Verify each product price
        for i in range(inventory_page.get_product_count()):
            name = inventory_page.get_product_name(i)
            actual_price = inventory_page.get_product_price(i)
            expected_price = expected_prices.get(name)

            assert expected_price is not None, f"Unknown product: {name}"
            assert actual_price == expected_price, \
                f"Price mismatch for {name}. Expected: ${expected_price}, Actual: ${actual_price}"

    @pytest.mark.inventory
    @pytest.mark.positive
    @pytest.mark.ui
    @allure.title("Product card layout")
    @allure.description("Verify product card contains all required elements")
    def test_product_card_elements(self, login_and_go_to_inventory, product_card_factory):
        """Test that product cards have all required elements."""
        inventory_page = login_and_go_to_inventory

        # Test first product card in detail
        card = product_card_factory.get_product_card_by_index(0)

        # Verify all elements are present
        assert card.is_visible(), "Product card not visible"
        assert card.get_name(), "Product name missing"
        assert card.get_description(), "Product description missing"
        assert card.get_price() > 0, "Product price missing or invalid"
        assert card.get_image_src(), "Product image source missing"
        assert card.add_to_cart_button.is_visible(), "Add to cart button missing"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Navigate to product details via name")
    @allure.description("Verify clicking product name navigates to detail page")
    def test_navigate_to_product_detail_by_name(self, login_and_go_to_inventory, product_detail_page):
        """Test navigation to product detail page by clicking product name."""
        inventory_page = login_and_go_to_inventory

        # Click on first product name
        first_product_name = inventory_page.get_product_name(0)
        inventory_page.click_product_name(first_product_name)

        # Verify navigation to detail page
        assert product_detail_page.product_name.is_visible(), "Product detail page not loaded"
        assert product_detail_page.get_product_name() == first_product_name, \
            "Wrong product detail page loaded"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Navigate to product details via image")
    @allure.description("Verify clicking product image navigates to detail page")
    def test_navigate_to_product_detail_by_image(self, login_and_go_to_inventory, product_detail_page):
        """Test navigation to product detail page by clicking product image."""
        inventory_page = login_and_go_to_inventory

        # Get product name for verification
        product_name = inventory_page.get_product_name(1)

        # Click on product image
        inventory_page.click_product_image(product_name)

        # Verify navigation to detail page
        assert product_detail_page.product_name.is_visible(), "Product detail page not loaded"
        assert product_detail_page.get_product_name() == product_name, \
            "Wrong product detail page loaded"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Return from product details")
    @allure.description("Verify can return to inventory from product detail page")
    def test_return_from_product_detail(self, login_and_go_to_inventory, product_detail_page):
        """Test returning to inventory from product detail page."""
        inventory_page = login_and_go_to_inventory

        # Navigate to product detail
        product_name = inventory_page.get_product_name(0)
        inventory_page.click_product_name(product_name)

        # Return to products
        product_detail_page.go_back_to_products()

        # Verify back on inventory page
        assert inventory_page.inventory_list.is_visible(), "Not returned to inventory page"
        assert inventory_page.get_product_count() == 6, "Inventory page not loaded properly"

    @pytest.mark.inventory
    @pytest.mark.positive
    @pytest.mark.critical
    @allure.title("Product images load correctly")
    @allure.description("Verify all product images load without errors")
    def test_product_images_load(self, login_and_go_to_inventory):
        """Test that all product images load correctly."""
        inventory_page = login_and_go_to_inventory

        # Verify we have products
        product_count = inventory_page.get_product_count()
        assert product_count > 0, "No products found"

        for i in range(product_count):
            product = inventory_page.inventory_items.nth(i)

            # Find any img tag within the product item
            images = product.locator("img")

            # Verify at least one image exists
            assert images.count() > 0, f"Product {i} has no image"

            # Get the first image (product image)
            image = images.first

            # Wait for image to be attached and visible
            image.wait_for(state="attached", timeout=5000)

            # Verify image has valid src attribute
            src = image.get_attribute("src")
            assert src, f"Product {i} image has no src attribute"
            assert len(src) > 0, f"Product {i} image has empty src"

            # Basic validation of src
            assert not src.endswith("404"), f"Product {i} image returns 404"
            assert ("/static/" in src or "/assets/" in src or src.startswith("http")), \
                f"Product {i} has unexpected src format: {src}"

    @pytest.mark.inventory
    @pytest.mark.positive
    @allure.title("Inventory page header elements")
    @allure.description("Verify inventory page header contains required elements")
    def test_inventory_header_elements(self, login_and_go_to_inventory, header_component):
        """Test inventory page header elements."""
        inventory_page = login_and_go_to_inventory

        # Verify header elements
        assert header_component.is_visible(), "Header not visible"
        assert header_component.is_menu_button_visible(), "Menu button not visible"
        assert header_component.is_logo_visible(), "App logo not visible"
        assert inventory_page.shopping_cart_link.is_visible(), "Cart link not visible"

        # Verify page title
        assert inventory_page.page_title.is_visible(), "Page title not visible"
        assert inventory_page.page_title.text_content() == "Products", \
            "Incorrect page title"