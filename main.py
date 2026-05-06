import os
import contextlib
import requests

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "bark-notifier",
    stateless_http=True,
    json_response=True,
)

BARK_KEY = os.getenv("BARK_KEY", "你的BarkKey")
BARK_SERVER = os.getenv("BARK_SERVER", "https://api.day.app")


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


async def home(request):
    return JSONResponse({
        "status": "ok",
        "message": "Bark MCP server is running",
        "mcp_url": "/mcp",
        "transport": "streamable-http"
    })


@contextlib.asynccontextmanager
async def lifespan(app):
    async with mcp.session_manager.run():
        yield


app = Starlette(
    routes=[
        Route("/", home),
        Mount("/", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)
