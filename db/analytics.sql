-- Daily aggregated skill demand
CREATE TABLE IF NOT EXISTS daily_skill_counts (
    skill TEXT NOT NULL,
    date DATE NOT NULL,
    job_count INTEGER NOT NULL,
    PRIMARY KEY (skill, date)
);
