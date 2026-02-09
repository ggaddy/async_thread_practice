import time
from concurrent.futures import ThreadPoolExecutor
from typing import List
import asyncio
from get_api import get_api, async_get_api

_API_URL = "http://localhost:8000"


def get_api_for_loop(calls: int = 15) -> List[dict]:
    results = [get_api(url=_API_URL) for i in range(calls)]
    return results


async def test_async_api_semaphore(calls: int = 15):
    limit = 20
    semaphore = asyncio.Semaphore(limit)

    async def run_with_semaphore() -> dict:
        async with semaphore:
            return await async_get_api(url=_API_URL)

    tasks = [run_with_semaphore() for i in range(calls)]
    results = await asyncio.gather(*tasks)
    return results


def main():
    # run in for loop and time
    print("===== For loop =====")
    start_time = time.time()
    results = get_api_for_loop(calls=15)
    end_time = time.time()
    for r in results:
        print(r)
    print(f"===== For loop elapsed time: {end_time - start_time}")

    # run in async and time
    print("===== async =====")
    start_time = time.time()
    results = asyncio.run(test_async_api_semaphore(calls=15))
    end_time = time.time()
    for r in results:
        print(r)
    print(f"===== async elapsed time: {end_time - start_time}")


if __name__ == "__main__":
    main()