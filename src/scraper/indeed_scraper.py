import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin
from ..db.db import insert_raw_posting

HEADERS_LIST = [
    # add multiple realistic user-agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
]

BASE = "https://de.indeed.com"

session = requests.Session()

def random_delay(min_s=1.0, max_s=3.0):
    time.sleep(random.uniform(min_s, max_s))

def fetch_search(query="data engineer", location="Freising"):
    params = {"q": query, "l": location}
    headers = {
        "User-Agent": random.choice(HEADERS_LIST),    
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
    resp = session.get(f"{BASE}/jobs", params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_search_page(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("a[data-jk]")  # selector may change; defensive code required
    results = []
    for a in cards:
        job_id = a.get("data-jk") or a.get("data-jobid") or a.get("id")
        href = a.get("href")
        job_url = urljoin(BASE, href) if href else None
        results.append({"job_id": job_id, "job_url": job_url})
    return results

def fetch_job_page(url):
    headers = {
        "User-Agent": random.choice(HEADERS_LIST),
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    resp = session.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def scrape_and_store(query="data engineer", location="Freising"):
    random_delay(2.0, 4.0)
    try:
        search_html = fetch_search(query, location)
    except Exception as e:
        print("Failed to fetch search page:", e)
        return
