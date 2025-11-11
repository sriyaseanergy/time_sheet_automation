import logging
from mcp.server.fastmcp import FastMCP
from mcp_provider.tools.toggle import fetch_toggl_tasks
from mcp_provider.tools.llm import rephrase_task_with_claude
from mcp_provider.tools.update_api import push_to_timesheet_api

logging.basicConfig(level=logging.INFO)
logging.getLogger("mcp").setLevel(logging.INFO)

app = FastMCP(name="toggl-claude-provider")

# Register tool 1: Fetch from Toggl
@app.tool()
def fetch_tasks(api_token: str):
    """Fetch recent Toggl tasks."""
    return fetch_toggl_tasks(api_token)

# Register tool 2: Rephrase with Claude
@app.tool()
def rephrase_task(description: str):
    """Rephrase a task description using Claude."""
    return rephrase_task_with_claude(description)

# Register tool 3: Push to your API
@app.tool()
def update_task(api_url: str, task_id: str, rephrased_text: str):
    """Push a rephrased task to your API endpoint."""
    return push_to_timesheet_api(api_url, task_id, rephrased_text)

# Optional ping tool for quick testing
@app.tool()
def ping() -> str:
    """Check provider health."""
    return "pong"

if __name__ == "__main__":
    print("Starting MCP provider: timesheet-agent (waiting for connection)...")
    app.run()
