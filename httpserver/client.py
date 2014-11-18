import threading

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def req():
    resp = requests.get('http://localhost:8085')
    # print(resp.content)
    return resp


if __name__=="__main__":
    futures = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        for x in range(10):
            futures.append(executor.submit(req))
        for future in as_completed(futures):
            data = future.result()
            print(data.content)
