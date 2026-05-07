import time

from selenium.webdriver.support.ui import WebDriverWait

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


def test_delete_note_ui(driver):
    config = get_config()

    login_to_application(driver, config)

    notes_page = ProductPage(driver)
    note_title = f"Delete Test {int(time.time())}"

    notes_page.create_note(
        note_title,
        "Testing delete functionality"
    )

    notes_page.wait_for_note_presence(
        note_title, timeout=config.get("timeout", 15)
    )

    initial_count = len(notes_page.get_all_notes())

    notes_page.delete_note_by_title(note_title)
    notes_page.wait_for_note_absence(
        note_title, timeout=config.get("timeout", 15)
    )

    updated_count = len(notes_page.get_all_notes())

    assert updated_count == initial_count - 1

def test_delete_note_by_title_ui(driver):
    config = get_config()

    login_to_application(driver, config)

    notes_page = ProductPage(driver)

    note_title = f"Delete Note {int(time.time())}"
    note_content = "Temporary note for delete test"

    notes_page.create_note(note_title, note_content)

    notes_page.wait_for_note_presence(
        note_title, timeout=config.get("timeout", 15)
    )

    notes_page.delete_note_by_title(note_title)

    notes_page.wait_for_note_absence(
        note_title, timeout=config.get("timeout", 15)
    )

    remaining_titles = [
        note.find_element(*ProductPage.NOTE_TITLE).text.strip()
        for note in notes_page.get_all_notes()
    ]

    assert note_title not in remaining_titles
