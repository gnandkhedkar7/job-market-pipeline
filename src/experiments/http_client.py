# Experimental HTTP client used during scraping exploration attempts (Indeed)
# Not used in v1 pipeline


import time
import random
import requests

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

class HttpClient:
    def __init__(self, timeout=10, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries

    def get(self, url: str) -> str | None:
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(
                    url,
                    headers=DEFAULT_HEADERS,
                    timeout=self.timeout,
                )

                if response.status_code == 200:
                    return response.text

                print(f"[WARN] Status {response.status_code} for {url}")

            except requests.RequestException as e:
                print(f"[ERROR] Attempt {attempt} failed: {e}")

            time.sleep(random.uniform(1, 3))  # polite delay

        return None
