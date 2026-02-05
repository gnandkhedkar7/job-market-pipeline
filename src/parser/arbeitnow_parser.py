from bs4 import BeautifulSoup
from sqlalchemy import text
from datetime import datetime, timezone

from src.db.db import engine, insert_parsed_job

SOURCE = "arbeitnow"

SELECT_RAW_SQL = """
SELECT
    job_id,
    job_url,
    raw_html
FROM raw_job_postings
WHERE source = :source
"""

def parse_job_html(html: str) -> tuple[str | None, str | None, str | None]:
    soup = BeautifulSoup(html, "html.parser")
    
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else None
    
    company_tag = soup.find("a", href=lambda x: x and "/companies/" in x)
    company = company_tag.get_text(strip=True) if company_tag else None
    
    location = None
    for li in soup.select("li"):
        text = li.get_text(strip=True)
        if "Germany" in text or "Remote" in text:
            location = text
            break
        
    return title, company, location

def parse_and_store_arbeitnow_jobs():
    with engine.begin() as conn:
        rows = conn.execute(
            text(SELECT_RAW_SQL),
            {"source": SOURCE},
        ).fetchall()
        
        for row in rows:
            title, company, location = parse_job_html(row.raw_html)
            
            insert_parsed_job(
                source=SOURCE,
                job_id=row.job_id,
                title=title,
                company=company,
                location=location,
                scraped_at=datetime.now(timezone.utc),
            )
            
    print("Arbeitnow job parsing complete.")
    
def main():
    parse_and_store_arbeitnow_jobs()
    
if __name__ == "__main__":
    main()