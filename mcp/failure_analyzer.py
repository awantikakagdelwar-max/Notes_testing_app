# mcp/failure_analyzer.py

from mcp.llm_client import LLMClient


class LLMFailureAnalyzer:

    @staticmethod
    def analyze(exception):

        prompt = f"""
        Analyze automation failure:

        {str(exception)}

        Suggest probable reason.
        """

        return LLMClient.generate(prompt)