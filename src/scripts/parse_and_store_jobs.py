from sqlalchemy import text
from src.db.db import engine, insert_parsed_job
from src.parser.indeed_parser import extract_job_cards

SOURCE = "indeed_de"

with engine.connect() as conn:
    rows = conn.execute(
        text("""
        SELECT raw_html, scraped_at
        FROM raw_job_postings
        WHERE source = :source
        LIMIT 1
        """),
        {"source": SOURCE},
    ).fetchall()

for raw_html, scraped_at in rows:
    job_cards = extract_job_cards(raw_html)

    for job in job_cards:
        insert_parsed_job(
            source=SOURCE,
            job_id=job["job_id"],
            title=job.get("title"),
            company=job.get("company"),
            location=job.get("location"),
            scraped_at=scraped_at,
        )

print("Parsed job postings inserted.")
