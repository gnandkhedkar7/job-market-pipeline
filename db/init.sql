CREATE TABLE IF NOT EXISTS raw_job_postings (
  id SERIAL PRIMARY KEY,
  source VARCHAR(64),
  scraped_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  job_id TEXT,
  raw_html TEXT,
  job_url TEXT,
  payload JSONB
);

CREATE UNIQUE INDEX IF NOT EXISTS raw_job_postings_jobid_source_idx
ON raw_job_postings (job_id, source);

CREATE TABLE IF NOT EXISTS parsed_job_postings (
  job_id TEXT NOT NULL,
  source TEXT NOT NULL,
  title TEXT,
  company TEXT,
  location TEXT,
  scraped_at TIMESTAMP WITH TIME ZONE,
  PRIMARY KEY (job_id, source)
);

CREATE TABLE IF NOT EXISTS daily_skill_counts (
  skill TEXT NOT NULL,
  date DATE NOT NULL,
  job_count INTEGER NOT NULL,
  PRIMARY KEY (skill, date)
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id TEXT NOT NULL,
    source TEXT NOT NULL,
    skill TEXT NOT NULL,
    extracted_from TEXT,
    scraped_at TIMESTAMPTZ,
    PRIMARY KEY (job_id, source, skill)
);

CREATE TABLE IF NOT EXISTS clean_job_postings (
    clean_job_id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    job_id TEXT NOT NULL,

    raw_title TEXT,
    normalized_title TEXT,

    company TEXT,
    location TEXT,

    scraped_at TIMESTAMPTZ,

    is_dropped BOOLEAN NOT NULL DEFAULT FALSE,
    drop_reason TEXT,

    UNIQUE (job_id, source)
);
