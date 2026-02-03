from sqlalchemy import text
from src.db.db import engine

QUERY = text("""
INSERT INTO daily_skill_counts (skill, date, job_count)
SELECT
    js.skill,
    DATE(js.scraped_at) AS date,
    COUNT(DISTINCT js.job_id) AS job_count
FROM job_skills js
GROUP BY js.skill, DATE(js.scraped_at)
ON CONFLICT (skill, date)
DO UPDATE SET job_count = EXCLUDED.job_count;
""")

def main():
    
    with engine.begin() as conn:
        conn.execute(QUERY)

    print("daily_skill_counts updated")

if __name__ == "__main__":
    main()