from sqlalchemy import text
from datetime import timezone
from src.db.db import engine
from src.cleaning.title_normalizer import normalize_title


SELECT_PARSED_SQL = """
SELECT
    job_id,
    source,
    title,
    company,
    location,
    scraped_at
FROM parsed_job_postings
"""


INSERT_CLEAN_SQL = """
INSERT INTO clean_job_postings (
    source,
    job_id,
    raw_title,
    normalized_title,
    company,
    location,
    scraped_at,
    is_dropped,
    drop_reason
)
VALUES (
    :source,
    :job_id,
    :raw_title,
    :normalized_title,
    :company,
    :location,
    :scraped_at,
    :is_dropped,
    :drop_reason
)
ON CONFLICT (job_id, source) DO NOTHING
"""


def clean_and_store_jobs():
    with engine.begin() as conn:

        rows = conn.execute(text(SELECT_PARSED_SQL)).fetchall()

        for row in rows:
            # ─────────────────────────────
            # STEP 4 — Title normalization
            # ─────────────────────────────
            normalized_title, drop_reason = normalize_title(row.title)

            # ─────────────────────────────
            # STEP 5 — Drop decision
            # ─────────────────────────────
            is_dropped = normalized_title is None

            params = {
                "source": row.source,
                "job_id": row.job_id,
                "raw_title": row.title,
                "normalized_title": normalized_title,
                "company": row.company,
                "location": row.location,
                "scraped_at": row.scraped_at.astimezone(timezone.utc)
                if row.scraped_at
                else None,
                "is_dropped": is_dropped,
                "drop_reason": drop_reason,
            }

            conn.execute(text(INSERT_CLEAN_SQL), params)

    print("Clean job postings inserted.")
    
def main():
    clean_and_store_jobs()


if __name__ == "__main__":
    clean_and_store_jobs()
