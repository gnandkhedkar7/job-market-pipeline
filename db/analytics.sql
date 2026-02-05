-- ============================================================
-- Analytics Queries for Job Market Pipeline (v1)
--
-- This file contains READ-ONLY analytics queries used to
-- inspect and understand skill demand trends.
--
-- Tables are created in db/init.sql
-- Aggregations are executed via Python pipeline code.
-- ============================================================


-- ------------------------------------------------------------
-- 1. Daily skill demand (logical definition)
-- ------------------------------------------------------------
-- This query is executed by src/analytics/build_daily_skill_counts.py
-- and materialized into the daily_skill_counts table.

-- INSERT INTO daily_skill_counts (skill, date, job_count)
-- SELECT
--     js.skill,
--     DATE(js.scraped_at) AS date,
--     COUNT(DISTINCT js.job_id) AS job_count
-- FROM job_skills js
-- GROUP BY js.skill, DATE(js.scraped_at)
-- ON CONFLICT (skill, date)
-- DO UPDATE SET job_count = EXCLUDED.job_count;


-- ------------------------------------------------------------
-- 2. Top in-demand skills (last 30 days)
-- ------------------------------------------------------------
SELECT
    skill,
    SUM(job_count) AS total_jobs
FROM daily_skill_counts
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY skill
ORDER BY total_jobs DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 3. Skill trends over time (for plotting)
-- ------------------------------------------------------------
SELECT
    skill,
    date,
    job_count
FROM daily_skill_counts
ORDER BY skill, date;


-- ------------------------------------------------------------
-- 4. City-wise skill demand
-- ------------------------------------------------------------
SELECT
    c.location,
    js.skill,
    COUNT(DISTINCT js.job_id) AS job_count
FROM job_skills js
JOIN clean_job_postings c
  ON js.job_id = c.job_id
 AND js.source = c.source
WHERE c.is_dropped = FALSE
GROUP BY c.location, js.skill
ORDER BY job_count DESC;
