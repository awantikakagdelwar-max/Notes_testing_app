from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.environment import get_config
from pages.login_page import LoginPage
from pages.product_page import ProductPage


def wait_for_page_load(driver, timeout):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def login_to_application(driver, config):
    driver.get(config["base_url"])
    wait_for_page_load(driver, config.get("timeout", 15))
    login_page = LoginPage(driver)
    login_page.login(config["email"], config["password"])


def test_empty_note_validation(driver):
    config = get_config()

    login_to_application(driver, config)

    notes_page = ProductPage(driver)

    # Wait until notes are loaded
    WebDriverWait(driver, config.get("timeout", 15)).until(
        lambda d: notes_page.get_all_notes() is not None
    )

    initial_count = len(notes_page.get_all_notes())

    notes_page.click(notes_page.ADD_NOTE)

    WebDriverWait(driver, config.get("timeout", 15)).until(
        EC.visibility_of_element_located(notes_page.TITLE)
    )

    notes_page.click(notes_page.SAVE)

    title_error = WebDriverWait(driver, config.get("timeout", 15)).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class,'invalid-feedback') and normalize-space(text())='Title is required']"
            )
        )
    )

    desc_error = WebDriverWait(driver, config.get("timeout", 15)).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class,'invalid-feedback') and normalize-space(text())='Description is required']"
            )
        )
    )

    assert title_error.is_displayed()
    assert desc_error.is_displayed()

    final_count = len(notes_page.get_all_notes())

    assert final_count == initial_count