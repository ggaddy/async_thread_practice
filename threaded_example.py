import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

from get_api import get_api

_API_URL = "http://localhost:8000"


def get_api_for_loop(calls: int = 15) -> List[dict]:
    results = [get_api(url=_API_URL) for i in range(calls)]
    return results


def get_api_threaded(calls: int = 15) -> List[dict]:
    with ThreadPoolExecutor(max_workers=15) as tpe:
        tpe_tasks = [tpe.submit(get_api, url=_API_URL) for i in range(calls)]
        tpe_results = [f.result() for f in tpe_tasks]
    return tpe_results


def main():
    # run in for loop and time
    print("===== For loop =====")
    start_time = time.time()
    results = get_api_for_loop(calls=15)
    end_time = time.time()
    for r in results:
        print(r)
    print(f"===== For loop elapsed time: {end_time - start_time}")

    # run in TPE and time
    print("===== ThreadPoolExecutor loop =====")
    start_time = time.time()
    results = get_api_threaded(calls=15)
    end_time = time.time()
    for r in results:
        print(r)
    print(f"===== ThreadPoolExecutor elapsed time: {end_time - start_time}")


if __name__ == "__main__":
    main()
