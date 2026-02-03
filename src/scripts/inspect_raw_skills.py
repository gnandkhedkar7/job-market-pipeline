from sqlalchemy import text
from src.db.db import engine

KEYWORDS = [
    "python",
    "sql",
    "excel",
    "docker",
    "aws",
    "java",
    "javaScript",
    "Microsoft",
    "cloud",
    "linux",
    "git",
]

with engine.connect() as conn:
    rows = conn.execute(
        text("""
        SELECT job_id, raw_html
        FROM raw_job_postings
        WHERE raw_html IS NOT NULL
        LIMIT 5
        """)
    ).fetchall()

for job_id, html in rows:
    print(f"\n--- Job {job_id} ---")
    lower = html.lower()
    found = [k for k in KEYWORDS if k in lower]
    print("Found keywords:", found)
