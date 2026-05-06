import os
import requests
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()

mcp = FastMCP("bark-notifier")

BARK_KEY = os.getenv("BARK_KEY")
BARK_SERVER = os.getenv("BARK_SERVER", "https://api.day.app")


@mcp.tool()
async def send_bark(title: str, body: str) -> str:
    """Send Bark notification"""

    if not BARK_KEY:
        return "Missing BARK_KEY"

    response = requests.post(
        f"{BARK_SERVER}/{BARK_KEY}",
        json={
            "title": title,
            "body": body,
            "group": "AI"
        },
        timeout=10
    )

    return response.text


app.mount("/mcp", mcp.sse_app())
