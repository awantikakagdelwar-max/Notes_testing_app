from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.product_page import ProductPage
from config.environment import get_config


def page_is_ready(driver):
    return driver.execute_script("return document.readyState") == "complete"


def test_create_note_ui(driver):
    config = get_config()

    driver.get(config["base_url"])
    WebDriverWait(driver, 15).until(page_is_ready)

    login_page = LoginPage(driver)
    login_page.login(config["email"], config["password"])

    notes_page = ProductPage(driver)

    note_title = "UI Test"
    note_description = "UI Description"

    notes_page.create_note(note_title, note_description)

    notes_list = notes_page.get_all_notes()

    assert len(notes_list) > 0