# Job Market Pipeline

A local, Docker-based data ingestion pipeline for collecting and storing raw job postings data.

This project is designed as a foundation for a job market analysis pipeline, with a strong focus on:

- reproducible local setup

- clean separation of concerns

- raw data preservation for future parsing and analytics

---

## Project Status

\*\*Current state:\*\*

- ✅ Python environment set up (`.venv`)

- ✅ PostgreSQL running via Docker Compose

- ✅ Database schema initialized

- ✅ Python → Database ingestion verified end-to-end

Scraping and parsing logic will be added incrementally on top of this foundation.

---

## Project Structure

job-market-pipeline/

├── src/

│ ├── db/

│ │ └── db.py # Database helper (SQLAlchemy Core)

│ ├── scraper/ # (planned) job site scrapers

│ └── scripts/

│ └── test_db.py # DB ingestion smoke test

│

├── db/

│ └── init.sql # Database schema initialization

│

├── docker-compose.yml # PostgreSQL via Docker

├── requirements.txt # Python dependencies

├── README.md

├── .gitignore

├── .env # Environment variables (not committed)

└── .venv/ # Python virtual environment (not committed)

---

## Database Design

The pipeline uses PostgreSQL with a \*\*raw ingestion table\*\*:

### `raw_job_postings`

This table stores unprocessed job data exactly as collected.

Columns:

- `source` – job site identifier (e.g. indeed_de)

- `job_id` – raw job ID from the source

- `job_url` – URL of the job posting

- `raw_html` – raw HTML of the job page

- `payload` – JSONB metadata (query, location, etc.)

- `scraped_at` – timestamp (auto-generated)

A unique constraint on `(job_id, source)` ensures idempotent inserts.

---

## Local Setup

### 1. Clone the repository

git clone <[text](https://github.com/gnandkhedkar7/job-market-pipeline.git)>

cd job-market-pipeline

### 2. Create and activate virtual environment

python -m venv .venv

# Windows (PowerShell)

.\\.venv\\Scripts\\Activate.ps1

### 3. Install Python dependencies

python -m pip install -r requirements.txt

#### 4. Create .env file (not committed)

POSTGRES_USER=pipeline_user

POSTGRES_PASSWORD=pipeline_pass

POSTGRES_DB=job_pipeline

POSTGRES_HOST=localhost

POSTGRES_PORT=5432

Start PostgreSQL with Docker

docker compose up -d

Verify that Postgres is running:

docker ps

Verifying the Database Connection

A simple ingestion test script is provided.

Run:

python -m src.scripts.test_db

Verify the inserted row directly in Postgres:

docker exec -it job_pipeline_postgres psql -U pipeline_user -d job_pipeline

SELECT \* FROM raw_job_postings;

Design Philosophy

Raw-first ingestion: store unmodified data before parsing

Dockerized infrastructure: consistent local setup

Minimal magic: SQLAlchemy Core instead of heavy ORM

Incremental development: validate each layer before adding complexity

## Analytics Pipeline

Build daily skill demand:
python -m src.analytics.build_daily_skill_counts


## Next Steps

Planned additions:

Job site scrapers (Indeed, etc.)

Retry and backoff logic

Structured parsing tables

Analytics and reporting layer
