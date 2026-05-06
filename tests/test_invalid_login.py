import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from config.environment import get_config
from pages.home_page import HomePage
from pages.login_page import LoginPage


def test_invalid_login(driver):
    config = get_config()

    driver.get(config["base_url"])
    WebDriverWait(driver, config.get("timeout", 15)).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    login = LoginPage(driver)
    login.login("invalid.user@example.com", "WrongPassword123!")

    # The app should remain on the login page for invalid credentials
    assert "/login" in driver.current_url

    # Verify the login form is still visible after the failed attempt
    assert login.wait(login.EMAIL).is_displayed()
    assert login.wait(login.PASSWORD).is_displayed()

    # Confirm home page did not load for invalid credentials
    home = HomePage(driver)
    with pytest.raises(TimeoutException):
        home.is_home_loaded()
