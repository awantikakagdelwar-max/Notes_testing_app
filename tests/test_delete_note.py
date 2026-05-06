import time

from selenium.webdriver.support.ui import WebDriverWait
from config.environment import get_config
from pages.login_page import LoginPage
from pages.product_page import ProductPage


def test_delete_note_ui(driver):
    config = get_config()

    driver.get(config["base_url"])
    WebDriverWait(driver, config.get("timeout", 15)).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    login = LoginPage(driver)
    login.login(config["email"], config["password"])

    notes = ProductPage(driver)
    initial_count = len(notes.get_all_notes())
    assert initial_count > 0

    # Delete the first note to verify delete-by-index functionality.
    notes.delete_first_note()

    WebDriverWait(driver, config.get("timeout", 15)).until(
        lambda d: len(notes.get_all_notes()) == initial_count - 1
    )

    assert len(notes.get_all_notes()) == initial_count - 1


def test_delete_note_by_title_ui(driver):
    config = get_config()

    driver.get(config["base_url"])
    WebDriverWait(driver, config.get("timeout", 15)).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    login = LoginPage(driver)
    login.login(config["email"], config["password"])

    notes = ProductPage(driver)
    target_title = f"Delete by title {int(time.time())}"
    notes.create_note(target_title, "Temporary note for delete by title")

    notes.wait_for_note_presence(target_title, timeout=config.get("timeout", 15))

    notes.delete_note_by_title(target_title)

    notes.wait_for_note_absence(target_title, timeout=config.get("timeout", 15))

    assert not any(
        note.find_element(*ProductPage.NOTE_TITLE).text.strip() == target_title
        for note in notes.get_all_notes()
    )
