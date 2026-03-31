"""
SmartApply AI - MCP Server
Exposes government scheme data as an MCP tool for ADK agents.
"""

import json
import os
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("smartapply_scheme_data_server")

# Load schemes database 
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.json")

def _load_schemes_data() -> list[dict]:
    """Load scheme data from JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@mcp.tool()
def get_all_schemes() -> list[dict]:
    """Retrieves all available government schemes."""
    return _load_schemes_data()

@mcp.tool()
def get_scheme_by_keyword(keyword: str) -> dict:
    """Search for government schemes based on a specific keyword.
    
    Use this tool when a user asks about agricultural, housing, health, or startup
    related criteria.
    """
    data = _load_schemes_data()
    lookup_key = keyword.strip().lower()
    
    matched_schemes = []
    for item in data:
        # Check title, description, or eligibility for keyword match
        if lookup_key in item.get("name", "").lower() or \
           lookup_key in item.get("description", "").lower() or \
           lookup_key in item.get("eligibility", "").lower():
            matched_schemes.append(item)
            
    if not matched_schemes:
        return {
            "error": f"No schemes found matching keyword '{keyword}'.",
            "suggestion": "Please try a broader category term."
        }
        
    return {
        "count": len(matched_schemes),
        "schemes": matched_schemes
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
