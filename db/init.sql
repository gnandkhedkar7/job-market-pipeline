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