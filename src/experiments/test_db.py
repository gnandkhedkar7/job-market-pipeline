# Deprecated: initial exploration with Indeed
# Not used in v1 pipeline

from src.db.db import insert_raw_posting

insert_raw_posting(
    source="test",
    job_id="job-123",
    job_url="https://example.com/job/123",
    raw_html="<html>test</html>",
    payload={
        "title": "Test Job",
        "company": "Test Co",
        "location": "Remote"
    },
)

print("Insert attempted successfully")
