"""
Logger configuration for the test framework.
Provides structured logging with different levels and formatters.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "test_automation", level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with file and console handlers.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # File handler with detailed format
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(
        log_dir / f"test_run_{timestamp}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Console handler with simple format
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Default logger instance
logger = setup_logger()


def log_test_start(test_name: str):
    """Log test execution start."""
    logger.info(f"{'='*60}")
    logger.info(f"Starting test: {test_name}")
    logger.info(f"{'='*60}")


def log_test_end(test_name: str, status: str):
    """Log test execution end."""
    logger.info(f"Test {test_name} completed with status: {status}")
    logger.info(f"{'='*60}")


def log_step(step_description: str):
    """Log a test step."""
    logger.info(f"Step: {step_description}")


def log_error(error_message: str, exception: Exception = None):
    """Log an error with optional exception details."""
    if exception:
        logger.error(f"{error_message}: {str(exception)}", exc_info=True)
    else:
        logger.error(error_message)


def log_warning(warning_message: str):
    """Log a warning message."""
    logger.warning(warning_message)


def log_debug(debug_message: str):
    """Log a debug message."""
    logger.debug(debug_message)