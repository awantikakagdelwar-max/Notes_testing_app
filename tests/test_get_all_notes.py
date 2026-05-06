import allure

from api.api_client import APIClient
from api.notes_api import NotesAPI
from config.environment import get_config


@allure.feature("Notes Management")
@allure.story("Retrieve All Notes from API")
def test_get_all_notes_api():
    config = get_config()

    client = APIClient(config["api_url"])
    client.login(config["email"], config["password"])

    notes_api = NotesAPI(client)
    response, response_time = notes_api.get_notes()

    assert response.status_code == 200

    data = response.json().get("data", [])

    allure.attach(
        f"Response time: {response_time:.2f}s",
        name="API Response Time",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        response.text,
        name="API Response JSON",
        attachment_type=allure.attachment_type.JSON
    )

    with allure.step("Notes Summary"):
        if data:
            table = "| Title | Description | Category | Completed | Created At |\n|-------|-------------|----------|-----------|------------|\n"
            for item in data:
                title = item.get("title", "N/A")
                description = item.get("description", "N/A")
                category = item.get("category", "N/A")
                completed = "Yes" if item.get("completed", False) else "No"
                created_at = item.get("created_at", "N/A")
                table += f"| {title} | {description} | {category} | {completed} | {created_at} |\n"

            allure.attach(
                table,
                name="All Notes",
                attachment_type=allure.attachment_type.TEXT
            )

            for index, item in enumerate(data, start=1):
                with allure.step(f"Note {index}: {item.get('title', 'Untitled')}"):
                    details = (
                        f"Title: {item.get('title', 'N/A')}\n"
                        f"Description: {item.get('description', 'N/A')}\n"
                        f"Category: {item.get('category', 'N/A')}\n"
                        f"Completed: {item.get('completed', False)}\n"
                        f"Created At: {item.get('created_at', 'N/A')}\n"
                        f"Updated At: {item.get('updated_at', 'N/A')}"
                    )

                    allure.attach(
                        details,
                        name=f"Note {index} Details",
                        attachment_type=allure.attachment_type.TEXT
                    )
        else:
            allure.attach(
                "No notes found",
                name="Notes Status",
                attachment_type=allure.attachment_type.TEXT
            )

    assert isinstance(data, list)