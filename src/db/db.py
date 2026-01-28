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
