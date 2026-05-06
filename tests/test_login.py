from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.environment import get_config
from selenium.webdriver.support.ui import WebDriverWait

def test_login(driver):
    config = get_config()

    driver.get(config["base_url"])
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    login = LoginPage(driver)
    login.login(config["email"], config["password"])

    home = HomePage(driver)

    assert home.is_home_loaded()