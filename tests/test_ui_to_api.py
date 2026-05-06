import time

from pages.login_page import LoginPage
from pages.product_page import ProductPage
from api.api_client import APIClient
from api.notes_api import NotesAPI
from config.environment import get_config
from selenium.webdriver.support.ui import WebDriverWait

def test_ui_to_api(driver):
    config = get_config()

    driver.get(config["base_url"])
    WebDriverWait(driver, 15).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    login = LoginPage(driver)
    login.login(config["email"], config["password"])

    notes = ProductPage(driver)

    title = "E2E Title"
    desc = "E2E Desc"

    notes.create_note(title, desc)
    notes.wait_for_note_presence(title, timeout=15)

    client = APIClient(config["api_url"])
    client.login(config["email"], config["password"])

    api = NotesAPI(client)
    res, _ = api.get_notes()

    data = res.json()["data"]

    assert any(note["title"] == title for note in data)

