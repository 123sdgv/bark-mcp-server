import os
import requests
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()

mcp = FastMCP("bark-notifier")

BARK_KEY = os.getenv("BARK_KEY", "你的BarkKey")
BARK_SERVER = os.getenv("BARK_SERVER", "https://api.day.app")


@app.get("/")
def health():
    return {
        "status": "ok",
        "message": "Bark MCP server is running",
        "sse_url": "/sse"
    }


@mcp.tool()
async def send_bark(title: str, body: str) -> str:
    """Send Bark notification to iPhone."""

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


app.mount("/", mcp.sse_app())
