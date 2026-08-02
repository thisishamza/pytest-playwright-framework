# Pytest Playwright Framework

A simple UI automation framework built with **Pytest + Playwright + Page Object Model (POM)**, using `.env` configuration and optional Docker execution.

## Tech Stack

- Python
- Pytest
- Playwright (sync API)
- pytest-playwright
- Allure reporting
- python-dotenv

## Project Structure

```text
pytest-playwright-framework/
├── fixtures/
│   └── pages.py               # Page object fixtures (login_page, home_page)
├── models/
│   ├── base_page.py           # Base page with common methods
│   └── pages/
│       ├── login_page.py      # Login page locators
│       └── home_page.py       # Home page locators
├── tests/
│   ├── conftest.py            # Browser/context/page + env fixtures
│   └── test_login_page.py     # UI + login flow tests
├── requirements.txt
├── pytest.ini
├── example.env
└── Dockerfile
```

## Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browser:
   ```bash
   playwright install chromium
   ```

4. Create `.env` file from `example.env`:
   ```env
   BASE_URL=https://www.saucedemo.com
   USERNAME=standard_user
   PASSWORD=secret_sauce
   ```

## Run Tests

Run all tests:

```bash
pytest
```

Run with marker:

```bash
pytest -m smoke
```

Run a specific test file:

```bash
pytest tests/test_login_page.py
```

## Allure Report

Generate Allure results while running tests:

```bash
pytest --alluredir=allure-results
```

Serve report:

```bash
allure serve allure-results
```

## Docker Run

Build image:

```bash
docker build -t pytest-playwright-framework .
```

Run tests in container:

```bash
docker run --rm --env-file .env pytest-playwright-framework
```

## Notes

- The framework uses Page Object Model for maintainable UI tests.
- `tests/conftest.py` currently launches Chromium with `headless=False` for local debugging.
- Docker command uses `xvfb-run` to provide a virtual display for browser execution.
