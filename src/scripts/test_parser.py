from sqlalchemy import text
from src.db.db import engine
from src.parser.indeed_parser import extract_title

with engine.connect() as conn:
    row = conn.execute(
        text("""
        SELECT raw_html, job_url
        FROM raw_job_postings
        LIMIT 1
    """)
    ).fetchone()


raw_html, job_url = row

print("Job URL:", job_url)
print("Raw HTML length:", len(raw_html) if raw_html else None)

# VERY IMPORTANT: inspect the HTML
print("\n--- HTML PREVIEW (first 500 chars) ---\n")
print(raw_html[:500])

title = extract_title(raw_html)

print("Extracted title:", title)
