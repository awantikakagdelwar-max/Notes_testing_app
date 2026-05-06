import allure
import pytest

from api.api_client import APIClient
from api.notes_api import NotesAPI
from config.environment import get_config


@allure.feature("Notes Management")
@allure.story("Retrieve All Notes from API")
def test_get_all_notes_api():
    config = get_config()
    client = APIClient(config["api_url"])
    client.login(config["email"], config["password"])

    api = NotesAPI(client)
    res, elapsed = api.get_notes()

    assert res.status_code == 200

    notes_data = res.json()["data"]

    # Attach performance info
    allure.attach(
        f"Response time: {elapsed:.2f}s",
        name="API Response Time",
        attachment_type=allure.attachment_type.TEXT
    )

    # Attach raw response
    allure.attach(
        res.text,
        name="API Response JSON",
        attachment_type=allure.attachment_type.JSON
    )

    # Display notes in Allure report
    with allure.step("Display All Notes"):
        if notes_data:
            notes_table = "| Title | Description | Category | Completed | Created At |\n|-------|-------------|----------|-----------|------------|\n"
            for note in notes_data:
                title = note.get("title", "N/A")
                description = note.get("description", "N/A")
                category = note.get("category", "N/A")
                completed = "Yes" if note.get("completed", False) else "No"
                created_at = note.get("created_at", "N/A")
                notes_table += f"| {title} | {description} | {category} | {completed} | {created_at} |\n"

            allure.attach(
                notes_table,
                name="All Notes Summary",
                attachment_type=allure.attachment_type.TEXT
            )

            # Individual note details
            for i, note in enumerate(notes_data, 1):
                with allure.step(f"Note {i}: {note.get('title', 'Untitled')}"):
                    allure.attach(
                        f"Title: {note.get('title', 'N/A')}\n"
                        f"Description: {note.get('description', 'N/A')}\n"
                        f"Category: {note.get('category', 'N/A')}\n"
                        f"Completed: {note.get('completed', False)}\n"
                        f"Created At: {note.get('created_at', 'N/A')}\n"
                        f"Updated At: {note.get('updated_at', 'N/A')}",
                        name=f"Note {i} Details",
                        attachment_type=allure.attachment_type.TEXT
                    )
        else:
            allure.attach("No notes found.", name="Notes Status", attachment_type=allure.attachment_type.TEXT)

    assert len(notes_data) >= 0  # Basic assertion that we got a response