"""
Screenshot capture utilities for test failures and documentation.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from playwright.sync_api import Page
from utils.logger import logger


class ScreenshotHelper:
    """Helper class for capturing screenshots during tests."""

    def __init__(self, page: Page, base_path: str = "reports/screenshots"):
        """
        Initialize screenshot helper.

        Args:
            page: Playwright page instance
            base_path: Base directory for saving screenshots
        """
        self.page = page
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def capture_screenshot(
        self,
        name: Optional[str] = None,
        full_page: bool = False,
        element: Optional[str] = None
    ) -> str:
        """
        Capture a screenshot of the page or specific element.

        Args:
            name: Custom name for the screenshot
            full_page: Whether to capture full page or viewport only
            element: Optional element selector to capture

        Returns:
            Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = name or f"screenshot_{timestamp}"

        # Ensure name has .png extension
        if not name.endswith('.png'):
            name = f"{name}.png"

        screenshot_path = self.base_path / name

        try:
            if element:
                # Capture specific element
                locator = self.page.locator(element)
                locator.screenshot(path=str(screenshot_path))
                logger.info(f"Element screenshot saved: {screenshot_path}")
            else:
                # Capture page
                self.page.screenshot(path=str(screenshot_path), full_page=full_page)
                logger.info(f"Page screenshot saved: {screenshot_path}")

            return str(screenshot_path)

        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            raise

    def capture_failure_screenshot(self, test_name: str) -> str:
        """
        Capture a screenshot on test failure.

        Args:
            test_name: Name of the failed test

        Returns:
            Path to the saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"failure_{test_name}_{timestamp}.png"

        # Create failures subdirectory
        failure_path = self.base_path / "failures"
        failure_path.mkdir(exist_ok=True)

        screenshot_path = failure_path / name

        try:
            # Capture full page for failures
            self.page.screenshot(path=str(screenshot_path), full_page=True)
            logger.error(f"Failure screenshot saved: {screenshot_path}")

            # Also log the page URL and title for context
            logger.error(f"Page URL: {self.page.url}")
            logger.error(f"Page Title: {self.page.title()}")

            return str(screenshot_path)

        except Exception as e:
            logger.error(f"Failed to capture failure screenshot: {e}")
            return ""

    def capture_comparison_screenshots(
        self,
        name: str,
        selectors: list,
        labels: Optional[list] = None
    ) -> list:
        """
        Capture multiple screenshots for comparison.

        Args:
            name: Base name for screenshots
            selectors: List of element selectors to capture
            labels: Optional labels for each screenshot

        Returns:
            List of paths to saved screenshots
        """
        screenshots = []
        labels = labels or [f"element_{i}" for i in range(len(selectors))]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for selector, label in zip(selectors, labels):
            filename = f"{name}_{label}_{timestamp}.png"
            path = self.capture_screenshot(name=filename, element=selector)
            screenshots.append(path)

        logger.info(f"Captured {len(screenshots)} comparison screenshots")
        return screenshots

    def capture_state_transition(
        self,
        action_name: str,
        before_action: callable,
        action: callable,
        after_action: callable = None
    ) -> tuple:
        """
        Capture screenshots before and after an action.

        Args:
            action_name: Name of the action being performed
            before_action: Function to execute before taking first screenshot
            action: The action to perform
            after_action: Optional function to execute after action

        Returns:
            Tuple of (before_screenshot_path, after_screenshot_path)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Execute before action if provided
        if before_action:
            before_action()

        # Capture before state
        before_path = self.capture_screenshot(
            name=f"{action_name}_before_{timestamp}"
        )

        # Perform the action
        action()

        # Execute after action if provided
        if after_action:
            after_action()

        # Capture after state
        after_path = self.capture_screenshot(
            name=f"{action_name}_after_{timestamp}"
        )

        logger.info(f"State transition captured for: {action_name}")
        return before_path, after_path

    def clean_old_screenshots(self, days: int = 7):
        """
        Clean screenshots older than specified days.

        Args:
            days: Number of days to keep screenshots
        """
        from datetime import timedelta
        import time

        cutoff_time = time.time() - (days * 24 * 60 * 60)

        cleaned_count = 0
        for screenshot in self.base_path.rglob("*.png"):
            if os.path.getmtime(screenshot) < cutoff_time:
                try:
                    screenshot.unlink()
                    cleaned_count += 1
                except Exception as e:
                    logger.warning(f"Could not delete screenshot {screenshot}: {e}")

        if cleaned_count > 0:
            logger.info(f"Cleaned {cleaned_count} old screenshots")

    def create_screenshot_report(self) -> dict:
        """
        Create a report of all screenshots in the directory.

        Returns:
            Dictionary with screenshot statistics
        """
        total_screenshots = 0
        failure_screenshots = 0
        total_size = 0

        for screenshot in self.base_path.rglob("*.png"):
            total_screenshots += 1
            total_size += screenshot.stat().st_size

            if "failure" in screenshot.name:
                failure_screenshots += 1

        report = {
            "total_screenshots": total_screenshots,
            "failure_screenshots": failure_screenshots,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "screenshot_directory": str(self.base_path)
        }

        logger.info(f"Screenshot report: {report}")
        return report