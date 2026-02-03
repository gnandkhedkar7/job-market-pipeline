from sqlalchemy import text
from src.db.db import engine
from src.cleaning.skill_dictionary import SKILLS


# We extract skills ONLY from raw_job_postings for now
SELECT_SQL = """
SELECT
    job_id,
    source,
    raw_html,
    scraped_at
FROM raw_job_postings
WHERE raw_html IS NOT NULL
"""


INSERT_SQL = """
INSERT INTO job_skills (
    job_id,
    source,
    skill,
    extracted_from,
    scraped_at
)
VALUES (
    :job_id,
    :source,
    :skill,
    :extracted_from,
    :scraped_at
)
ON CONFLICT DO NOTHING
"""


def extract_skills_from_html(html: str) -> set[str]:
    if not html:
        return set()

    html_lower = html.lower()
    found = set()

    for skill in SKILLS:
        if skill in html_lower:
            found.add(skill)

    return found


def extract_and_store_skills():
    total_jobs = 0
    jobs_with_no_skills = 0
    total_skills_inserted = 0

    with engine.begin() as conn:
        rows = conn.execute(text(SELECT_SQL)).fetchall()

        for row in rows:
            total_jobs += 1

            skills = extract_skills_from_html(row.raw_html)

            if not skills:
                jobs_with_no_skills += 1
                continue

            for skill in skills:
                conn.execute(
                    text(INSERT_SQL),
                    {
                        "job_id": row.job_id,
                        "source": row.source,
                        "skill": skill,
                        "extracted_from": "description",
                        "scraped_at": row.scraped_at,
                    },
                )
                total_skills_inserted += 1

    print(
        f"Skill extraction complete.\n"
        f"Jobs processed: {total_jobs}\n"
        f"Jobs with zero skills: {jobs_with_no_skills}\n"
        f"Total skills inserted: {total_skills_inserted}"
    )


if __name__ == "__main__":
    extract_and_store_skills()
