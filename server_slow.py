"""Async Starlette server that responds with a random u32 after a delay."""

from __future__ import annotations

import asyncio
import random

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

MIN_DELAY_SECONDS = 0.1
MAX_DELAY_SECONDS = 2.0
U32_MAX = 2**32 - 1


async def slow_random_response(request) -> JSONResponse:
    """Return a JSON response containing a random u32 after a short delay."""
    delay = random.uniform(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
    await asyncio.sleep(delay)
    value = random.randint(0, U32_MAX)
    return JSONResponse({"value": value, "delay_seconds": f"{delay:.3f}"})


routes = [Route("/", slow_random_response)]
app = Starlette(debug=False, routes=routes)


def main() -> None:
    """Run the Uvicorn server for local development."""
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    main()
