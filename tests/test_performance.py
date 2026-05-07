import time

from pages.home_page import HomePage
from pages.login_page import LoginPage
from config.environment import get_config


def test_ui_login_performance(driver):
    config = get_config()

    # Open app
    driver.get(config["base_url"])

    login_page = LoginPage(driver)

    # Start timing
    start_time = time.time()

    login_page.login(config["email"], config["password"])

    # Wait until the home page is loaded after login
    home_page = HomePage(driver)
    assert home_page.is_home_loaded(), "Login did not complete successfully"

    # Stop timing
    total_time = time.time() - start_time

    max_time = float(config.get("ui_login_threshold", 20))

    assert total_time < max_time, (
        f"UI login is slow: took {total_time:.2f}s (limit: {max_time}s)"
    )