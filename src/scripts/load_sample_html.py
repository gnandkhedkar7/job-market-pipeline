from pathlib import Path
from src.db.db import insert_raw_posting

BASE_DIR = Path(__file__).resolve().parents[2]
SAMPLE_PATH = BASE_DIR / "src" / "samples" / "job_sample.html"

with open(SAMPLE_PATH, encoding="utf-8") as f:
    html = f.read()

insert_raw_posting(
    source="indeed_de",
    job_id="sample-1",
    job_url="file://src/samples/job_sample.html",
    raw_html=html,
    payload={"source": "manual_sample"},
)

print("Sample HTML inserted")
