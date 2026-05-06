import time

from pages.login_page import LoginPage
from pages.product_page import ProductPage
from api.api_client import APIClient
from api.notes_api import NotesAPI
from config.environment import get_config
from selenium.webdriver.support.ui import WebDriverWait


def test_api_to_ui(driver):
    config = get_config()

    client = APIClient(config["api_url"])
    client.login(config["email"], config["password"])

    api = NotesAPI(client)
    title = f"API E2E {int(time.time())}"
    description = "Created through API"
    res, _ = api.create_note(title, description, category="Home")
    assert res.status_code == 200

    driver.get(config["base_url"])
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    login = LoginPage(driver)
    login.login(config["email"], config["password"])

    notes = ProductPage(driver)
    notes.wait_for_note_presence(title, timeout=15)

    note_titles = [note.find_element(*notes.NOTE_TITLE).text.strip() for note in notes.get_all_notes()]

    assert title in note_titles