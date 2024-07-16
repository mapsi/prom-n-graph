import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor

SERVICES = [
    "http://node-express:3000",
    "http://python-flask:8000"
]


def make_request(url):
    try:
        response = requests.get(url)
        print(f"Request to {url}: Status {response.status_code}")
    except requests.RequestException as e:
        print(f"Request to {url} failed: {str(e)}")


def generate_traffic():
    while True:
        with ThreadPoolExecutor(max_workers=5) as executor:
            for _ in range(random.randint(1, 10)):
                url = random.choice(SERVICES)
                executor.submit(make_request, url)
        time.sleep(random.uniform(0.1, 1))


if __name__ == "__main__":
    print("Traffic generator started")
    generate_traffic()
