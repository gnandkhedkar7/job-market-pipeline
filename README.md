\# Job Market Pipeline



A local, Docker-based data ingestion pipeline for collecting and storing raw job postings data.



This project is designed as a foundation for a job market analysis pipeline, with a strong focus on:

\- reproducible local setup

\- clean separation of concerns

\- raw data preservation for future parsing and analytics



---



\## Project Status



\*\*Current state:\*\*  

\- ✅ Python environment set up (`.venv`)

\- ✅ PostgreSQL running via Docker Compose

\- ✅ Database schema initialized

\- ✅ Python → Database ingestion verified end-to-end



Scraping and parsing logic will be added incrementally on top of this foundation.



---



\## Project Structure



job-market-pipeline/

├── src/

│ ├── db/

│ │ └── db.py # Database helper (SQLAlchemy Core)

│ ├── scraper/ # (planned) job site scrapers

│ └── scripts/

│ └── test\_db.py # DB ingestion smoke test

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



\## Database Design



The pipeline uses PostgreSQL with a \*\*raw ingestion table\*\*:



\### `raw\_job\_postings`



This table stores unprocessed job data exactly as collected.



Columns:

\- `source` – job site identifier (e.g. indeed\_de)

\- `job\_id` – raw job ID from the source

\- `job\_url` – URL of the job posting

\- `raw\_html` – raw HTML of the job page

\- `payload` – JSONB metadata (query, location, etc.)

\- `scraped\_at` – timestamp (auto-generated)



A unique constraint on `(job\_id, source)` ensures idempotent inserts.



---



\## Local Setup



\### 1. Clone the repository

git clone <repo-url>

cd job-market-pipeline



\### 2. Create and activate virtual environment 

python -m venv .venv



\# Windows (PowerShell)

.\\.venv\\Scripts\\Activate.ps1



\### 3. Install Python dependencies

python -m pip install -r requirements.txt





\#### 4. Create .env file (not committed)

POSTGRES\_USER=pipeline\_user

POSTGRES\_PASSWORD=pipeline\_pass

POSTGRES\_DB=job\_pipeline

POSTGRES\_HOST=localhost

POSTGRES\_PORT=5432



Start PostgreSQL with Docker

docker compose up -d





Verify that Postgres is running:



docker ps



Verifying the Database Connection



A simple ingestion test script is provided.



Run:



python -m src.scripts.test\_db



Verify the inserted row directly in Postgres:



docker exec -it job\_pipeline\_postgres psql -U pipeline\_user -d job\_pipeline



SELECT \* FROM raw\_job\_postings;



Design Philosophy



Raw-first ingestion: store unmodified data before parsing



Dockerized infrastructure: consistent local setup



Minimal magic: SQLAlchemy Core instead of heavy ORM



Incremental development: validate each layer before adding complexity



\## Next Steps



Planned additions:



Job site scrapers (Indeed, etc.)



Retry and backoff logic



Structured parsing tables



Analytics and reporting layer



