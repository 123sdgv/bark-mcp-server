import os
import requests

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

BARK_KEY = os.getenv("BARK_KEY")
BARK_SERVER = os.getenv("BARK_SERVER", "https://api.day.app")

RAILWAY_HOST = "bark-mcp-server-production.up.railway.app"

mcp = FastMCP(
    "bark-notifier",
    stateless_http=True,
    json_response=True,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8000")),
    path="/mcp",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            RAILWAY_HOST,
            f"{RAILWAY_HOST}:*",
            "localhost:*",
            "127.0.0.1:*",
        ],
        allowed_origins=[
            f"https://{RAILWAY_HOST}",
            f"https://{RAILWAY_HOST}:*",
            "http://localhost:*",
            "http://127.0.0.1:*",
        ],
    ),
)


@mcp.tool()
async def send_bark(title: str, body: str) -> str:
    """Send a Bark notification to iPhone."""

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


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
