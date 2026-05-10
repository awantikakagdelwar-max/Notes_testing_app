import pytest

from mcp.test_data_generator import (
    MCPTestDataGenerator
)


@pytest.mark.mcp
def test_generate_mcp_test_data():

    data = (
        MCPTestDataGenerator
        .generate_note()
    )

    assert data["title"] is not None

    assert data["description"] is not None

    assert data["category"] == "Work"