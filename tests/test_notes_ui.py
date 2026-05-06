from pages.login_page import LoginPage
from pages.product_page import ProductPage
from config.environment import get_config
from selenium.webdriver.support.ui import WebDriverWait
def test_create_note_ui(driver):
    config = get_config()

    driver.get(config["base_url"])
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    login = LoginPage(driver)
    login.login(config["email"], config["password"])

    notes = ProductPage(driver)

    notes.create_note("UI Test", "UI Description")

    assert len(notes.get_all_notes()) > 0