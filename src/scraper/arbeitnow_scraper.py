from playwright.sync_api import sync_playwright
from datetime import datetime, timezone
from src.db.db import insert_raw_posting

SOURCE = "arbeitnow"
START_URL = "https://www.arbeitnow.com/jobs"

def scrape_arbeitnow(max_jobs=20):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Opening Arbeitnow job listings...")
        page.goto(START_URL, timeout=60000)
        page.wait_for_load_state("networkidle")
        
        job_cards = page.locator("li.list-none")
        total = job_cards.count()
        print(f"Found {total} job cards")
        
        job_links = []
        for i in range(min(total, max_jobs)):
            href = job_cards.nth(i).locator("a").first.get_attribute("href")
            if href:
                job_links.append(href)
                
        print(f"Collected {len(job_links)} job URLs")
        
        for url in job_links:
            try:
                print("Fetching job:", url)
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle")
                
                html = page.content()
                
                insert_raw_posting(
                    source=SOURCE,
                    job_id=url,
                    job_url=url,
                    raw_html=html,
                    payload={
                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                        "source_type": "playwright",
                        "site": "arbeitnow",
                    },
                )
                
            except Exception as e:
                print("Failed job:", url, e)
                
        browser.close()
        print("Arbeitnow scraping completed.")
        
if __name__ == "__main__":
    scrape_arbeitnow()