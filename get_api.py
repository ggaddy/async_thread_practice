import asyncio
import time

import httpx
import requests


def get_api(url: str = "", retries: int = 3, timeout: int = 2) -> dict:
    # set the timeout less than 2 seconds to simulate an unreliable remote server
    # the server has a delay between 0.1-1.0 seconds
    result = {"code": "", "result": "", "error": ""}
    attempt_count = max(1, retries)
    for attempt in range(attempt_count):
        is_last_attempt = attempt == attempt_count - 1
        try:
            response = requests.get(url=url, timeout=timeout)
            response.raise_for_status()
            result["code"] = response.status_code
            result["result"] = response.json()
            result["error"] = ""
            return result
        # lets only backoff if we hit a ConnectTimeout or ReadTimeout
        except (requests.ConnectionError, requests.ConnectTimeout) as err:
            result["error"] = str(err)
            if is_last_attempt:
                return result
            backoff = 0.1 * (2**attempt)
            print(
                f"get_api|RequestException: {err}|attempt: {attempt + 1}/{attempt_count}|backoff: {backoff}"
            )
            time.sleep(backoff)
        except requests.RequestException as err:
            result["error"] = str(err)
            if is_last_attempt:
                return result
            print(
                f"get_api|RequestException: {err}|attempt: {attempt + 1}/{attempt_count}"
            )


async def async_get_api(url: str = "", retries: int = 3, timeout: int = 2) -> dict:
    # set the timeout less than 2 seconds to simulate an unreliable remote server
    # the server has a delay between 0.1-1.0 seconds
    result = {"code": "", "result": "", "error": ""}
    attempt_count = max(1, retries)
    for attempt in range(attempt_count):
        is_last_attempt = attempt == attempt_count - 1
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, timeout=timeout)
                response.raise_for_status()
                result["code"] = response.status_code
                result["result"] = response.json()
                result["error"] = ""
                return result
        # handle exceptions from httpx
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.RequestError) as err:
            result["error"] = str(err)
            if is_last_attempt:
                return result
            # lets only backoff if we hit a ConnectTimeout or ReadTimeout
            if isinstance(err, (httpx.ConnectError, httpx.ConnectTimeout)):
                backoff = 0.1 * (2**attempt)
                print(
                    f"async_get_api|RequestException: {err}|attempt: {attempt + 1}/{attempt_count}|backoff: {backoff}"
                )
                await asyncio.sleep(backoff)
            else:
                print(
                    f"async_get_api|RequestException: {err}|attempt: {attempt + 1}/{attempt_count}"
                )
