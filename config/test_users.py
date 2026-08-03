"""
Test user configuration for Saucedemo application.
Contains all 6 test users with their expected behaviors.
"""

from typing import Dict, Any


class TestUsers:
    """Test user personas and their configurations."""

    # Common password for all test users
    PASSWORD = "secret_sauce"

    # User configurations with expected behaviors
    USERS: Dict[str, Dict[str, Any]] = {
        "standard_user": {
            "username": "standard_user",
            "password": PASSWORD,
            "expected_behavior": "normal",
            "can_login": True,
            "can_checkout": True,
            "has_performance_issues": False,
            "has_visual_issues": False,
            "description": "Standard user with normal application behavior"
        },
        "locked_out_user": {
            "username": "locked_out_user",
            "password": PASSWORD,
            "expected_behavior": "locked",
            "can_login": False,
            "can_checkout": False,
            "has_performance_issues": False,
            "has_visual_issues": False,
            "error_message": "Epic sadface: Sorry, this user has been locked out.",
            "description": "User account that has been locked out"
        },
        "problem_user": {
            "username": "problem_user",
            "password": PASSWORD,
            "expected_behavior": "buggy",
            "can_login": True,
            "can_checkout": False,  # Has issues with lastname field
            "has_performance_issues": False,
            "has_visual_issues": False,
            "checkout_issue": "lastname_field_error",
            "description": "User that experiences bugs in checkout process"
        },
        "performance_glitch_user": {
            "username": "performance_glitch_user",
            "password": PASSWORD,
            "expected_behavior": "slow",
            "can_login": True,
            "can_checkout": True,
            "has_performance_issues": True,
            "has_visual_issues": False,
            "expected_delay": 3000,  # Expected delay in milliseconds
            "description": "User experiencing slow performance"
        },
        "error_user": {
            "username": "error_user",
            "password": PASSWORD,
            "expected_behavior": "errors",
            "can_login": True,
            "can_checkout": False,
            "has_performance_issues": False,
            "has_visual_issues": False,
            "description": "User that triggers application errors"
        },
        "visual_user": {
            "username": "visual_user",
            "password": PASSWORD,
            "expected_behavior": "visual_bugs",
            "can_login": True,
            "can_checkout": True,
            "has_performance_issues": False,
            "has_visual_issues": True,
            "description": "User experiencing visual/UI inconsistencies"
        }
    }

    @classmethod
    def get_user(cls, username: str) -> Dict[str, Any]:
        """
        Get user configuration by username.

        Args:
            username: Username to get configuration for

        Returns:
            User configuration dictionary

        Raises:
            ValueError: If username not found
        """
        if username not in cls.USERS:
            raise ValueError(f"User '{username}' not found in test users")
        return cls.USERS[username]

    @classmethod
    def get_standard_users(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get users that can successfully login and perform normal operations.

        Returns:
            Dictionary of users that can login
        """
        return {
            name: config
            for name, config in cls.USERS.items()
            if config["can_login"] and config["expected_behavior"] in ["normal", "slow"]
        }

    @classmethod
    def get_problematic_users(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get users with known issues or special behaviors.

        Returns:
            Dictionary of problematic users
        """
        return {
            name: config
            for name, config in cls.USERS.items()
            if config["expected_behavior"] != "normal"
        }

    @classmethod
    def get_users_that_can_login(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all users that can successfully login.

        Returns:
            Dictionary of users that can login
        """
        return {
            name: config
            for name, config in cls.USERS.items()
            if config["can_login"]
        }

    @classmethod
    def get_users_that_cannot_login(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get users that cannot login.

        Returns:
            Dictionary of users that cannot login
        """
        return {
            name: config
            for name, config in cls.USERS.items()
            if not config["can_login"]
        }

    @classmethod
    def get_users_that_can_checkout(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get users that can complete checkout.

        Returns:
            Dictionary of users that can complete checkout
        """
        return {
            name: config
            for name, config in cls.USERS.items()
            if config["can_checkout"]
        }

    @classmethod
    def get_all_usernames(cls) -> list:
        """
        Get list of all usernames.

        Returns:
            List of all usernames
        """
        return list(cls.USERS.keys())

    @classmethod
    def get_user_for_parametrize(cls) -> list:
        """
        Get user data formatted for pytest parametrize.

        Returns:
            List of tuples (username, password, expected_behavior)
        """
        return [
            (config["username"], config["password"], config["expected_behavior"])
            for config in cls.USERS.values()
        ]