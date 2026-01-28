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
