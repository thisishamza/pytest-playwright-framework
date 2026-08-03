"""
Test data loader and constants for the test framework.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class TestData:
    """Centralized test data management."""

    # Base paths
    DATA_DIR = Path(__file__).parent

    # URLs
    BASE_URL = "https://www.saucedemo.com"
    INVENTORY_URL = f"{BASE_URL}/inventory.html"
    CART_URL = f"{BASE_URL}/cart.html"
    CHECKOUT_STEP_ONE_URL = f"{BASE_URL}/checkout-step-one.html"
    CHECKOUT_STEP_TWO_URL = f"{BASE_URL}/checkout-step-two.html"
    CHECKOUT_COMPLETE_URL = f"{BASE_URL}/checkout-complete.html"

    # Error messages
    LOCKED_OUT_ERROR = "Epic sadface: Sorry, this user has been locked out."
    USERNAME_REQUIRED_ERROR = "Epic sadface: Username is required"
    PASSWORD_REQUIRED_ERROR = "Epic sadface: Password is required"
    INVALID_CREDENTIALS_ERROR = "Epic sadface: Username and password do not match any user in this service"
    FIRST_NAME_REQUIRED_ERROR = "Error: First Name is required"
    LAST_NAME_REQUIRED_ERROR = "Error: Last Name is required"
    POSTAL_CODE_REQUIRED_ERROR = "Error: Postal Code is required"

    # Success messages
    CHECKOUT_COMPLETE_HEADER = "Thank you for your order!"
    CHECKOUT_COMPLETE_TEXT = "Your order has been dispatched, and will arrive just as fast as the pony can get there!"

    @classmethod
    def load_json_file(cls, filename: str) -> Dict[str, Any]:
        """
        Load JSON data from file.

        Args:
            filename: Name of JSON file in data directory

        Returns:
            Parsed JSON data as dictionary
        """
        file_path = cls.DATA_DIR / filename
        with open(file_path, 'r') as f:
            return json.load(f)

    @classmethod
    def get_users_data(cls) -> Dict[str, Any]:
        """Get all users test data."""
        return cls.load_json_file("users.json")

    @classmethod
    def get_products_data(cls) -> Dict[str, Any]:
        """Get all products test data."""
        return cls.load_json_file("products.json")

    @classmethod
    def get_checkout_data(cls) -> Dict[str, Any]:
        """Get all checkout test data."""
        return cls.load_json_file("checkout_data.json")

    @classmethod
    def get_valid_users(cls) -> Dict[str, Any]:
        """Get valid test users."""
        users = cls.get_users_data()
        return users.get("test_users", {})

    @classmethod
    def get_invalid_users(cls) -> Dict[str, Any]:
        """Get invalid test users."""
        users = cls.get_users_data()
        return users.get("invalid_users", {})

    @classmethod
    def get_product_list(cls) -> List[Dict[str, Any]]:
        """Get list of all products."""
        products = cls.get_products_data()
        return products.get("products", [])

    @classmethod
    def get_product_by_name(cls, name: str) -> Dict[str, Any]:
        """
        Get product by name.

        Args:
            name: Product name

        Returns:
            Product data dictionary

        Raises:
            ValueError: If product not found
        """
        products = cls.get_product_list()
        for product in products:
            if product["name"] == name:
                return product
        raise ValueError(f"Product '{name}' not found")

    @classmethod
    def get_sorted_products(cls, sort_type: str) -> List[str]:
        """
        Get expected product order for sort type.

        Args:
            sort_type: Sort type (az, za, lohi, hilo)

        Returns:
            List of product names in expected order
        """
        products = cls.get_products_data()
        sort_orders = products.get("sort_orders", {})
        return sort_orders.get(sort_type, [])

    @classmethod
    def get_valid_checkout_data(cls) -> List[Dict[str, Any]]:
        """Get valid checkout test data sets."""
        checkout = cls.get_checkout_data()
        return checkout.get("valid_data", [])

    @classmethod
    def get_invalid_checkout_data(cls) -> List[Dict[str, Any]]:
        """Get invalid checkout test data sets."""
        checkout = cls.get_checkout_data()
        return checkout.get("invalid_data", [])

    @classmethod
    def get_checkout_edge_cases(cls) -> List[Dict[str, Any]]:
        """Get checkout edge case test data."""
        checkout = cls.get_checkout_data()
        return checkout.get("edge_cases", [])

    @classmethod
    def calculate_tax(cls, subtotal: float) -> float:
        """
        Calculate tax for given subtotal.

        Args:
            subtotal: Subtotal amount

        Returns:
            Tax amount
        """
        products = cls.get_products_data()
        tax_rate = products.get("tax_rate", 0.08)
        return round(subtotal * tax_rate, 2)

    @classmethod
    def calculate_total(cls, subtotal: float) -> float:
        """
        Calculate total including tax.

        Args:
            subtotal: Subtotal amount

        Returns:
            Total amount including tax
        """
        tax = cls.calculate_tax(subtotal)
        return round(subtotal + tax, 2)

    @classmethod
    def get_cheapest_product(cls) -> Dict[str, Any]:
        """Get the cheapest product."""
        products = cls.get_product_list()
        return min(products, key=lambda x: x["price"])

    @classmethod
    def get_most_expensive_product(cls) -> Dict[str, Any]:
        """Get the most expensive product."""
        products = cls.get_product_list()
        return max(products, key=lambda x: x["price"])