"""
SmartApply AI Agent - ADK Agent with MCP Integration
"""

import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioConnectionParams
from mcp import StdioServerParameters

# Path to the MCP server script
MCP_SERVER_SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "mcp_service",
    "mcp_main.py"
)

AGENT_INSTRUCTION = """You are SmartApply AI, a specialized decision intelligence agent that helps citizens
make informed decisions about government scheme applications and eligibility.

Your capabilities:
1. Fetch available government schemes using the get_all_schemes tool.
2. Search for schemes using specific keywords with the get_scheme_by_keyword tool.
3. Compare different schemes side by side if applicable.
4. Provide a clear, actionable recommendation.

How to respond:
- Provide exact criteria matched using the data parsed from tools.
- Never make up data or eligibility logic not strictly listed in the tool results.
"""

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="smartapply_agent",
    instruction=AGENT_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="python",
                    args=[MCP_SERVER_SCRIPT],
                ),
                timeout=15,
            ),
        )
    ],
)
