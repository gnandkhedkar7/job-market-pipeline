from datetime import datetime, timezone
from sqlalchemy import text
from src.scraper.http_client import HttpClient
from src.db.db import engine

BASE_URL = "https://de.indeed.com"
SOURCE = "indeed_de"

INSERT_SQL = """
INSERT INTO raw_job_postings (
    job_id,
    source,
    job_url,
    raw_html,
    scraped_at
)
VALUES (
    :job_id,
    :source,
    :job_url,
    :raw_html,
    :scraped_at
)
ON CONFLICT (job_id, source) DO NOTHING
"""

class IndeedScraper:
    def __init__(self):
        self.client = HttpClient()

    def build_search_url(self, query: str, location: str) -> str:
        return (
            f"{BASE_URL}/jobs?"
            f"q={query.replace(' ', '+')}&"
            f"l={location.replace(' ', '+')}"
        )

    def scrape_search_page(self, query: str, location: str):
        url = self.build_search_url(query, location)
        html = self.client.get(url)

        if not html:
            print("[ERROR] Failed to fetch search page")
            return

        job_id = f"search-{hash(url)}"

        with engine.begin() as conn:
            conn.execute(
                text(INSERT_SQL),
                {
                    "job_id": job_id,
                    "source": SOURCE,
                    "job_url": url,
                    "raw_html": html,
                    "scraped_at": datetime.now(timezone.utc),
                },
            )

        print(f"[OK] Stored search page for {query} in {location}")
