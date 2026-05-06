from api.api_client import APIClient
from api.notes_api import NotesAPI
from config.environment import get_config

def test_get_notes_api():
    config = get_config()

    client = APIClient(config["api_url"])

    client.register(config["email"], config["password"])
    client.login(config["email"], config["password"])

    api = NotesAPI(client)

    res, time_taken = api.get_notes()

    assert res.status_code == 200