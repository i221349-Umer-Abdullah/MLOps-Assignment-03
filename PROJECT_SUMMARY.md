# MLOps Assignment 3 - NASA APOD ETL Pipeline
## Project Summary

**Student**: i221349 - Umer Abdullah
**Course**: MLOps (Semester 07)
**Submission Date**: November 16, 2025
**Status**: ✅ Operational - Running in Cloud

---

## Overview

Fully automated ETL pipeline that extracts daily NASA Astronomy Picture of the Day (APOD) data, transforms it, loads to PostgreSQL and CSV, versions with DVC, and commits metadata to Git.

### Architecture

```
NASA APOD API (Extract)
    ↓
Data Transformation (Transform)
    ↓
Dual Storage (Load)
├── Neon PostgreSQL (Cloud)
└── CSV File (Local)
    ↓
DVC Versioning (Version)
    ↓
Git Commit (Commit)
```

---

## Implementation Details

### 5 Sequential Tasks (Airflow DAG)

1. **Extract**: Fetch data from NASA APOD API using DEMO_KEY
2. **Transform**: Clean and standardize JSON data to structured format
3. **Load**: Persist to PostgreSQL (cloud) + CSV file (with DVC tracking)
4. **DVC Version**: Track CSV file changes with Data Version Control
5. **Git Commit**: Commit DVC metadata (.dvc files) to version control

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Orchestration | Apache Airflow | 3.1.2+astro.1 |
| Cloud Platform | Astronomer | Runtime 3.1-4 |
| Database | Neon PostgreSQL | Serverless (Cloud) |
| Data Versioning | DVC | 3.64.0 |
| Version Control | Git/GitHub | - |
| Python | Python | 3.12 |
| Data Processing | Pandas | 2.2.0 |
| HTTP Client | Requests | >=2.32.0 |
| PostgreSQL Driver | psycopg2-binary | 2.9.9 |

---

## Deployment

### Cloud Infrastructure

**Astronomer Cloud**
- Region: AWS ap-southeast-1
- Deployment ID: `cmhyv4tge0vjj01ka2izdq47g`
- Airflow UI: https://cmhyv36ur0viz01kawg1ffecd.astronomer.run/dizdq47g
- Schedule: Daily at 00:00 UTC (automatic)
- Status: Healthy ✅

**Neon PostgreSQL**
- Type: Serverless PostgreSQL
- Region: ap-southeast-1
- Database: neondb
- Table: apod_data
- Free Tier: 0.5GB storage, 100 compute hours/month
- Auto-suspend: After 5 minutes inactivity

**GitHub Repository**
- URL: https://github.com/i221349-Umer-Abdullah/MLOps-Assignment-03
- Visibility: Public
- Main Branch: `main`

---

## Assignment Requirements Compliance

| Requirement | Implementation | Status |
|------------|----------------|--------|
| Extract from API | NASA APOD API with requests library | ✅ |
| Transform data | Pandas DataFrame transformation | ✅ |
| Load to PostgreSQL | Neon PostgreSQL cloud database | ✅ |
| Load to CSV | Local CSV file in `include/` directory | ✅ |
| DVC versioning | Track CSV with `dvc add` command | ✅ |
| Git commits | Automated commit of .dvc metadata | ✅ |
| Airflow orchestration | 5 sequential tasks in DAG | ✅ |
| Astronomer deployment | Cloud deployment on Astronomer | ✅ |
| Daily automation | Scheduled daily runs | ✅ |
| Documentation | Complete docs and issue tracking | ✅ |

---

## Key Design Decisions

### 1. Cloud Database Choice: Neon PostgreSQL
**Rationale**: Assignment requires PostgreSQL, but cloud deployment needs external database
- **Evaluated**: AWS RDS, Google Cloud SQL, Neon, Supabase
- **Chosen**: Neon PostgreSQL
- **Reasons**:
  - Free tier sufficient for project (0.5GB, 100 hours/month)
  - Serverless architecture (auto-suspend when idle)
  - No credit card required
  - Compatible with psycopg2
  - Completely cloud-based (no local PC dependency)

### 2. DVC Storage: Local Storage
**Rationale**: Assignment doesn't specify remote DVC storage
- Using local `.dvc/cache` directory
- Remote storage (S3, GCS) not required for assignment
- Could be extended to remote storage if needed

### 3. API Key: DEMO_KEY
**Rationale**: NASA provides DEMO_KEY for testing/development
- Rate limit: 30 requests/hour, 50 requests/day
- Sufficient for daily pipeline (1 request/day)
- Production would use registered API key

### 4. GitHub Actions Removed
**Rationale**: Using Astronomer Cloud, not GitHub Actions
- Initial implementation included GitHub Actions workflow
- Removed due to token scope limitation and redundancy
- Astronomer handles scheduling and execution

---

## Challenges Faced & Solutions

See [ISSUES_AND_FIXES.md](ISSUES_AND_FIXES.md) for detailed issue tracking.

**Major Issues (12 total)**:
1. Python dependency version conflicts (Airflow 3.x)
2. Airflow 3.x breaking changes (4 deprecations)
3. Docker networking and port conflicts
4. Git repository unavailable in containers
5. PostgreSQL vs SQLite architecture decision
6. GitHub token workflow scope limitation

**All issues resolved** ✅

---

## How to Demo (2 Weeks From Now)

### 1. Show GitHub Repository
- URL: https://github.com/i221349-Umer-Abdullah/MLOps-Assignment-03
- Show commit history, code structure

### 2. Show Astronomer Cloud Dashboard
- Login: https://cloud.astronomer.io
- Navigate to deployment
- Show ~14 successful daily runs

### 3. Show Airflow UI
- URL: https://cmhyv36ur0viz01kawg1ffecd.astronomer.run/dizdq47g
- Show DAG with 5 tasks
- Trigger manual run (demonstrate live)
- Show execution logs

### 4. Show PostgreSQL Data
- Login to Neon: https://console.neon.tech
- SQL Editor query:
```sql
SELECT COUNT(*) FROM apod_data;  -- Should show ~14 rows
SELECT date, title FROM apod_data ORDER BY date DESC LIMIT 5;
```

### 5. Show DVC Versioning
- Show `include/apod_data.csv.dvc` file in repository
- Explain DVC tracking mechanism
- Show `.dvc/config` for remote storage configuration

---

## Files Overview

```
.
├── dags/
│   └── nasa_apod_pipeline.py      # Main DAG with 5 tasks
├── include/
│   ├── apod_data.csv              # Historical data (tracked by DVC)
│   └── apod_data.csv.dvc          # DVC metadata file
├── .dvc/
│   ├── config                     # DVC configuration
│   └── .gitignore                 # DVC cache ignored
├── requirements.txt               # Python dependencies
├── packages.txt                   # System packages (git)
├── Dockerfile                     # Astronomer Runtime base
├── .astro/                        # Astronomer configuration
├── ISSUES_AND_FIXES.md           # Complete issue tracking
├── PROJECT_SUMMARY.md            # This file
└── GITHUB_ACTIONS_DEPLOYMENT.md  # Historical reference
```

---

## Monitoring & Verification

### Daily Automated Runs
- **Schedule**: Every day at 00:00 UTC
- **Expected**: 14 runs by 2025-11-28
- **Check Status**: Airflow UI > DAGs > nasa_apod_cloud_pipeline

### Data Accumulation
- **PostgreSQL**: Query `SELECT COUNT(*) FROM apod_data;`
- **CSV File**: Check `include/apod_data.csv` row count
- **DVC**: Check `.dvc/cache/` directory size

### Health Checks
1. Astronomer deployment status: https://cloud.astronomer.io
2. Neon database status: https://console.neon.tech
3. GitHub repository: Verify latest commits

---

## Future Enhancements (Post-Assignment)

1. **Remote DVC Storage**: Add S3/GCS backend for DVC
2. **API Key Management**: Use registered NASA API key (higher limits)
3. **Data Quality Checks**: Add Great Expectations for validation
4. **Monitoring**: Integrate with Prometheus/Grafana
5. **Alerting**: Add email/Slack notifications for failures
6. **CI/CD**: Automated testing before deployment
7. **Data Transformations**: Add more sophisticated data cleaning
8. **Multiple Data Sources**: Integrate additional NASA APIs

---

## Conclusion

Complete MLOps pipeline implementing:
- ✅ Automated data extraction
- ✅ Data transformation
- ✅ Dual storage (PostgreSQL + CSV)
- ✅ Data versioning (DVC)
- ✅ Git integration
- ✅ Cloud deployment (Astronomer)
- ✅ Production-ready architecture

**Assignment Status**: Complete and operational
**Last Updated**: 2025-11-14
**Demo Date**: 2025-11-28 (or as scheduled)
