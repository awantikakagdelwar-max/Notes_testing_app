import time


class MCPTestDataGenerator:

    @staticmethod
    def generate_note():

        timestamp = int(time.time())

        return {
            "title": f"MCP_Note_{timestamp}",
            "description": (
                f"Generated MCP note "
                f"{timestamp}"
            ),
            "category": "Work"
        }