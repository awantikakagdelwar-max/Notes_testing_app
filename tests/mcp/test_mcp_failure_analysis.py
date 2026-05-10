import pytest

from mcp.failure_analyzer import (
    LLMFailureAnalyzer
)


@pytest.mark.mcp
def test_mcp_failure_analysis():

    error = (
        "TimeoutException: "
        "Element not found"
    )

    result = (
        LLMFailureAnalyzer
        .analyze(error)
    )

    assert (
        "AI Response Generated"
        in result
    )