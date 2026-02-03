import os
import json
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "pipeline_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "pipeline_pass")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "job_pipeline")

CONN_STR = (
    f"postgresql+psycopg2://{DB_USER}:"
    f"{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    CONN_STR,
    pool_size=5,
    max_overflow=10,
    future=True,
)

def insert_raw_posting(
    source: str,
    job_id: str,
    job_url: str,
    raw_html: str,
    payload: dict,
) -> None:
    insert_sql = text("""
        INSERT INTO raw_job_postings (source, job_id, job_url, raw_html, payload)
        VALUES (:source, :job_id, :job_url, :raw_html, :payload)
        ON CONFLICT (job_id, source) DO NOTHING
    """)

    try:
        with engine.begin() as conn:
            conn.execute(
                insert_sql,
                {
                    "source": source,
                    "job_id": job_id,
                    "job_url": job_url,
                    "raw_html": raw_html,
                    "payload": json.dumps(payload),
                },
            )
    except SQLAlchemyError as e:
        print("DB insert error:", e)

def insert_parsed_job(
    source: str,
    job_id: str,
    title: str | None,
    company: str | None,
    location: str | None,
    scraped_at,
) -> None:
    insert_sql = text("""
        INSERT INTO parsed_job_postings (
            job_id,
            source,
            title,
            company,
            location,
            scraped_at
        )
        values (
            :job_id,
            :source,
            :title,
            :company,
            :location,
            :scraped_at
        )
        ON CONFLICT (job_id, source) DO NOTHING
    """)
    try:
        with engine.begin() as conn:
            conn.execute(
                insert_sql,
                {
                    "job_id": job_id,
                    "source": source,
                    "title" : title,
                    "company": company,
                    "location": location,
                    "scraped_at": scraped_at,
                },    
            )
            
    except SQLAlchemyError as e: 
        print("Parsed insert error: ", e)

def insert_clean_job(
    source: str,
    job_id: str,
    raw_title: str | None,
    normalized_title: str | None,
    company: str | None,
    location: str | None,
    scraped_at,
    is_dropped: bool,
    drop_reason: str | None,
) -> None:
    insert_sql = text("""
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
    """)

    with engine.begin() as conn:
        conn.execute(
            insert_sql,
            {
                "source": source,
                "job_id": job_id,
                "raw_title": raw_title,
                "normalized_title": normalized_title,
                "company": company,
                "location": location,
                "scraped_at": scraped_at,
                "is_dropped": is_dropped,
                "drop_reason": drop_reason,
            },
        )