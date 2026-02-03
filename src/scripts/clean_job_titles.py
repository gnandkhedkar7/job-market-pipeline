from sqlalchemy import text
from src.db.db import engine, insert_clean_job
from src.cleaning.title_normalizer import normalize_title

SOURCE = "indeed_de"

with engine.connect() as conn:
    rows = conn.execute(
        text("""
        SELECT job_id, title, company, location, scraped_at
        FROM parsed_job_postings
        WHERE source = :source
        """),
        {"source": SOURCE},
    ).fetchall()

for job_id, title, company, location, scraped_at in rows:
    normalized_title, drop_reason = normalize_title(title)

    insert_clean_job(
        source=SOURCE,
        job_id=job_id,
        raw_title=title,
        normalized_title=normalized_title,
        company=company,
        location=location,
        scraped_at=scraped_at,
        is_dropped=drop_reason is not None,
        drop_reason=drop_reason,
    )

print("Clean job postings inserted.")
