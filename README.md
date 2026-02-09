# Async vs Threaded API Calls

This project compares sequential, threaded, and async approaches to calling a
slow local API. Start the demo server first, then run the threaded or async
client scripts to compare timings.

## Prerequisites

- Python 3.10+
- Install dependencies with uv (if you haven't already):

```bash
uv sync
```

## Run the slow API server

Open a terminal and start the Starlette server on port 8000:

```bash
uv run python server_slow.py
```

## Run the threaded example

In a second terminal (with the server still running), execute:

```bash
uv run python threaded_example.py
```

This prints the results and elapsed times for the sequential loop versus the
`ThreadPoolExecutor` version.

## Run the async example

In another terminal (with the server still running), execute:

```bash
uv run python async_example.py
```

This prints the results and elapsed times for the sequential loop versus the
async `asyncio.gather` approach.