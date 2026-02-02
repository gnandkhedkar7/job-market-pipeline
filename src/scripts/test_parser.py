from sqlalchemy import text
from src.db.db import engine
from src.parser.indeed_parser import extract_page_title
from src.parser.indeed_parser import extract_job_titles, extract_job_cards

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

page_title = extract_page_title(raw_html)
print("Page <title>:", page_title)

titles = extract_job_titles(raw_html)
print(f"Found {len(titles)} job titles:")
for t in titles[:5]:
    print("-", t)

job_cards = extract_job_cards(raw_html)

print(f"Found {len(job_cards)} job cards")
for job in job_cards[:5]:
    print(job)