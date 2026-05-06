import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from config.environment import get_config
from pages.home_page import HomePage
from pages.login_page import LoginPage


def page_is_loaded(driver):
    return driver.execute_script("return document.readyState") == "complete"


def wait_for_page_ready(driver, timeout):
    WebDriverWait(driver, timeout).until(page_is_loaded)


invalid_credentials = [
    ("invalid.user@example.com", "WrongPassword123!"),
    ("", "ValidPassword123!"),
    ("valid.user@example.com", ""),
    ("invalid@", "short"),
    
]


@pytest.mark.parametrize("email,password", invalid_credentials)
def test_invalid_login(driver, email, password):
    config = get_config()

    driver.get(config["base_url"])
    wait_for_page_ready(driver, config.get("timeout", 15))

    login_page = LoginPage(driver)
    login_page.login(email, password)

    assert "/login" in driver.current_url

    email_visible = login_page.wait(login_page.EMAIL).is_displayed()
    password_visible = login_page.wait(login_page.PASSWORD).is_displayed()

    assert email_visible
    assert password_visible

    home_page = HomePage(driver)

    with pytest.raises(TimeoutException):
        home_page.is_home_loaded()