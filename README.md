# Job Market Data Pipeline

An end-to-end, containerized data pipeline that scrapes real-world job postings, cleans and normalizes noisy data, extracts in-demand skills, and produces daily skill-demand analytics using PostgreSQL.

This project is designed to demonstrate real-world data engineering practices: resilient ingestion, structured transformations, explicit data quality handling, and reproducible automation.

---

## 🚀 Features

- Scrape and store raw HTML job postings
- Parse job listings from search result pages
- Normalize job titles and explicitly handle dropped records
- Extract skills from job descriptions
- Generate daily skill-demand analytics
- Fully automated using Docker Compose
- Idempotent and restart-safe pipeline

---

## 🏗️ Architecture Overview

```text

.
Scraper (Playwright)
        ↓
raw_job_postings
        ↓
Parser
        ↓
parsed_job_postings
        ↓
Cleaner
        ↓
clean_job_postings
        ↓
Skill Extractor
        ↓
job_skills
        ↓
daily_skill_counts

```

Each stage persists its output to PostgreSQL, enabling easy debugging, replay, and auditing.

---

## Data Source

- **Arbeitnow (public job boards for jobs in Germany)**
- **Scraped using Playwright (headless Chromium)**

---

## 🧱 Tech Stack

- **Python 3.12**
- **PostgreSQL 15**
- **SQLAlchemy**
- **Playwright**
- **BeautifulSoup**
- **Docker & Docker Compose**

---

## 📂 Project Structure

```text

.
├── db/
│ ├── init.sql # Database schema (sourceof truth)
│ └── analytics.sql # Analytics queries
├── src/
│ ├── analytics/ # Analysis logic
│ ├── db/ # Database utilities
│ ├── parser/ # HTML parsing logic
│ ├── cleaning/ # Normalization & skill extraction
│ ├── experiments/ # Non-production experiments
│ ├── scraper/ # Scraper logic
│ └── scripts/ # Pipeline orchestration
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env # Not committed
├── .gitignore
└── README.md
```

---

## 🗄️ Database Tables

### Core Tables

- `raw_job_postings` — raw HTML snapshots
- `parsed_job_postings` — extracted job metadata
- `clean_job_postings` — normalized titles with drop flags
- `job_skills` — exploded skills per job
- `daily_skill_counts` — aggregated analytics

All tables are created in **`db/init.sql`**.

---

## ▶️ How to Run the Pipeline

### 1️⃣ Start services

```bash
docker compose up --build
```

### 2️⃣ Run scraper manually

```bash
docker compose run pipeline python -m src.scraper.arbeitnow_scraper
```

### 3️⃣ Run the full pipeline

```bash
docker compose run pipeline
```

The pipeline will: 1. Parse jobs 2. Clean and normalize titles 3. Extract skills 4. Update daily skill analytics

## 🔍 Inspecting the Database

```bash
docker exec -it job_pipeline_postgres psql -U pipeline_user -d job_pipeline
```

Example checks

```bash
SELECT COUNT(*) FROM clean_job_postings;
SELECT COUNT(*) FROM job_skills;
SELECT * FROM daily_skill_counts ORDER BY date DESC, job_count DESC;
```

## 📊 Example Analytics

Top skills (latest day):

```bash
SELECT *
FROM daily_skill_counts
ORDER BY date DESC, job_count DESC
LIMIT 10;
```

## 🧪 Data Quality Handling

    * Titles are normalized using rule-based logic
    * Jobs with missing or invalid titles are explicitly dropped
    * Drop reasons are stored (missing_title, title_too_short, etc.)
    * Jobs with zero extracted skills are logged

## 🔁 Reproducibility

The database schema is fully defined in db/init.sql.

To reset everything from scratch:

```bash
docker compose down -v
docker compose up --build
```

## 📌 Design Principles

    * Explicit data states (raw → parsed → clean)
    * No silent failures
    * SQL-first analytics
    * Simple, explainable logic over premature ML

## Project Status
    
    * ✅ v1 complete
    * 🔜 v2: additional job boards, trend analysis, optional dashboard

## 🔮 Future Extensions (Optional)

    * Scheduled runs (cron / Prefect)
    * Streamlit dashboard
    * Skill trend detection
    * Role clustering using TF-IDF

## 👤 Author

**Gauri Nandkhedkar**  
GitHub: [@gauri-nandkhedkar](https://github.com/gauri-nandkhedkar)  
LinkedIn: [@gauri-nandkhedkar](https://www.linkedin.com/in/gauri-nandkhedkar/)
