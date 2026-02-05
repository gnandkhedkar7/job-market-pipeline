# Deprecated: initial exploration with Indeed
# Not used in v1 pipeline

from sqlalchemy import text
from src.db.db import engine
from src.experiments.indeed_parser import extract_job_cards, extract_page_title

with engine.connect() as conn:
    row = conn.execute(
        text("""
        SELECT raw_html, job_url
        FROM raw_job_postings
        WHERE job_id = 'sample-1'
        """)
    ).fetchone()

raw_html, job_url = row

print("Job URL:", job_url)
print("Raw HTML length:", len(raw_html))
print("Page <title>:", extract_page_title(raw_html))

job_cards = extract_job_cards(raw_html)

print(f"\nFound {len(job_cards)} job cards:")
for job in job_cards[:5]:
    print(job)
