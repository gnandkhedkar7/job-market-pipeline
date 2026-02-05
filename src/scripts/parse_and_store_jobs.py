from sqlalchemy import text
from src.db.db import engine, insert_parsed_job
from src.experiments.indeed_parser import extract_job_cards

SOURCE = "indeed_de"


def parse_and_store_jobs():
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
            SELECT raw_html, scraped_at
            FROM raw_job_postings
            WHERE source = :source
            """),
            {"source": SOURCE},
        ).fetchall()

    for raw_html, scraped_at in rows:
        if not raw_html:
            continue

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


def main():
    parse_and_store_jobs()


if __name__ == "__main__":
    main()
