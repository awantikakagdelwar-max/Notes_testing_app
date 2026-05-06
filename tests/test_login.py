from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.environment import get_config


def page_is_loaded(driver):
    return driver.execute_script("return document.readyState") == "complete"


def test_login(driver):
    config = get_config()

    driver.get(config["base_url"])
    WebDriverWait(driver, 15).until(page_is_loaded)

    login_page = LoginPage(driver)
    login_page.login(config["email"], config["password"])

    home_page = HomePage(driver)

    assert home_page.is_home_loaded()