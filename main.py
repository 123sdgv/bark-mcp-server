import os
import requests

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

BARK_KEY = os.getenv("BARK_KEY")
BARK_SERVER = os.getenv("BARK_SERVER", "https://api.day.app")

mcp = FastMCP(
    "bark-notifier",
    stateless_http=True,
    json_response=True,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8000")),
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
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
