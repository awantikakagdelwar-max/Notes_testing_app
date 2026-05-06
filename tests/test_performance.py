import time

from pages.login_page import LoginPage
from api.api_client import APIClient
from api.notes_api import NotesAPI
from config.environment import get_config


def test_notes_api_performance():
    config = get_config()
    client = APIClient(config["api_url"])
    client.login(config["email"], config["password"])
    api = NotesAPI(client)

    res, elapsed = api.get_notes()

    assert res.status_code == 200
    assert elapsed < float(config.get("performance_threshold", 1.5)), (
        f"Notes API response time is too slow: {elapsed:.2f}s"
    )


def test_ui_login_performance(driver):
    config = get_config()
    start = time.time()

    driver.get(config["base_url"])
    login = LoginPage(driver)
    login.login(config["email"], config["password"])

    elapsed = time.time() - start

    assert elapsed < float(config.get("ui_login_threshold", 8.0)), (
        f"UI login flow is too slow: {elapsed:.2f}s"
    )
