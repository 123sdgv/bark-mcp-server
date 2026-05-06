import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("bark-notifier")

BARK_KEY = os.getenv("BARK_KEY")
BARK_SERVER = os.getenv("BARK_SERVER", "https://api.day.app")


@mcp.tool()
def send_bark(title: str, body: str) -> str:
    """Send a notification to iPhone via Bark."""
    if not BARK_KEY:
        return "BARK_KEY is not configured."

    url = f"{BARK_SERVER}/{BARK_KEY}"
    resp = requests.post(
        url,
        json={
            "title": title,
            "body": body,
            "group": "AI",
        },
        timeout=10,
    )

    if resp.ok:
        return "Notification sent successfully."
    return f"Failed: {resp.status_code} {resp.text}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
