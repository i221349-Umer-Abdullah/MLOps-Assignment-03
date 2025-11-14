# NASA APOD ETL Pipeline - MLOps Assignment 3

**Course**: MLOps (Semester 07)
**Student**: i221349 - Umer Abdullah
**Submission Date**: November 16, 2025
**Status**: ✅ Operational

---

## Overview

Automated ETL pipeline that extracts daily NASA Astronomy Picture of the Day (APOD) data, transforms it, loads to PostgreSQL and CSV, versions with DVC, and commits metadata to Git. Deployed on Astronomer Cloud for continuous daily execution.

### Live Deployment

- **Airflow UI**: https://cmhyv36ur0viz01kawg1ffecd.astronomer.run/dizdq47g
- **Schedule**: Daily at 00:00 UTC (automatic)
- **Database**: Neon PostgreSQL (Serverless Cloud)

---

## Architecture

```
NASA APOD API
    ↓
[Extract Task] → Get daily astronomy picture data
    ↓
[Transform Task] → Clean & standardize data
    ↓
[Load Task] → Save to Neon PostgreSQL + CSV
    ↓
[DVC Version Task] → Track CSV with DVC
    ↓
[Git Commit Task] → Commit .dvc metadata
```

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Orchestration | Apache Airflow | 3.1.2+astro.1 |
| Cloud Platform | Astronomer | Runtime 3.1-4 |
| Database | Neon PostgreSQL | Serverless |
| Data Versioning | DVC | 3.64.0 |
| Language | Python | 3.12 |
| Data Processing | Pandas | 2.2.0 |

---

## Project Structure

```
.
├── dags/
│   └── nasa_apod_pipeline.py      # Main DAG with 5 sequential tasks
├── include/
│   ├── apod_data.csv              # Historical data (DVC tracked)
│   └── apod_data.csv.dvc          # DVC metadata
├── .dvc/
│   └── config                     # DVC configuration
├── requirements.txt               # Python dependencies
├── packages.txt                   # System packages (git)
├── Dockerfile                     # Astronomer Runtime
├── PROJECT_SUMMARY.md            # Complete project overview
├── ISSUES_AND_FIXES.md           # Issue tracking & solutions
└── GITHUB_ACTIONS_DEPLOYMENT.md  # Alternative deployment guide
```

---

## Features

✅ **5 Sequential Tasks**:
1. Extract data from NASA APOD API
2. Transform JSON to structured format
3. Load to PostgreSQL + CSV (dual persistence)
4. Version CSV with DVC
5. Commit DVC metadata to Git

✅ **Cloud Deployment**: Runs 24/7 on Astronomer Cloud (AWS ap-southeast-1)
✅ **PostgreSQL Integration**: Neon serverless database (free tier)
✅ **Data Versioning**: DVC for data lineage tracking
✅ **Automated Scheduling**: Daily execution without manual intervention
✅ **Complete Documentation**: Issues, fixes, and architecture details

---

## Quick Start

### Prerequisites

- Docker Desktop
- Astronomer CLI (`astro`)
- Git

### Local Development

1. **Clone the repository**:
```bash
git clone https://github.com/i221349-Umer-Abdullah/MLOps-Assignment-03.git
cd MLOps-Assignment-03
```

2. **Start Airflow locally**:
```bash
astro dev start
```

3. **Access Airflow UI**:
- URL: http://localhost:8080
- Username: `admin`
- Password: `admin`

4. **Trigger the DAG**:
- Find `nasa_apod_cloud_pipeline`
- Click the play button to run manually

### Cloud Deployment

Already deployed! Access at: https://cmhyv36ur0viz01kawg1ffecd.astronomer.run/dizdq47g

---

## Assignment Requirements Compliance

| Requirement | Status |
|------------|--------|
| Extract from API | ✅ |
| Transform data | ✅ |
| Load to PostgreSQL | ✅ |
| Load to CSV | ✅ |
| DVC versioning | ✅ |
| Git commits | ✅ |
| Airflow orchestration | ✅ |
| Astronomer deployment | ✅ |
| Daily automation | ✅ |
| Documentation | ✅ |

---

## Documentation

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**: Complete project overview, architecture, and design decisions
- **[ISSUES_AND_FIXES.md](ISSUES_AND_FIXES.md)**: Detailed issue tracking with 12 resolved problems
- **[GITHUB_ACTIONS_DEPLOYMENT.md](GITHUB_ACTIONS_DEPLOYMENT.md)**: Alternative deployment approach

---

## Key Design Decisions

### 1. Neon PostgreSQL
- **Why**: Assignment requires PostgreSQL; cloud deployment needs external DB
- **Benefits**: Free tier, serverless, auto-suspend, no local PC needed

### 2. DVC with Local Storage
- **Why**: Assignment doesn't specify remote storage
- **Benefits**: Simple setup, meets requirements

### 3. Astronomer Cloud
- **Why**: 24/7 execution without keeping PC on
- **Benefits**: Professional MLOps platform, automatic scheduling, monitoring

---

## Challenges & Solutions

**Major Issues Resolved**:
- Airflow 3.x breaking changes (4 deprecations)
- Docker networking conflicts
- PostgreSQL vs SQLite architecture decision
- Git repository unavailability in containers
- GitHub token scope limitations

See [ISSUES_AND_FIXES.md](ISSUES_AND_FIXES.md) for complete details.

---

## Demo Instructions

### For Demo Day (2 Weeks From Now)

1. **Show GitHub Repository**
   - This repository with complete code

2. **Show Astronomer Dashboard**
   - Login: https://cloud.astronomer.io
   - ~14 successful daily runs

3. **Show Airflow UI**
   - Live DAG execution
   - Task logs and status

4. **Show PostgreSQL Data**
   - Neon dashboard: https://console.neon.tech
   - Query: `SELECT COUNT(*) FROM apod_data;`

5. **Show DVC Versioning**
   - `include/apod_data.csv.dvc` file
   - DVC configuration

---

## Monitoring

**Check Pipeline Status**:
- Astronomer UI: https://cloud.astronomer.io
- Airflow UI: https://cmhyv36ur0viz01kawg1ffecd.astronomer.run/dizdq47g
- Neon Dashboard: https://console.neon.tech

**Expected Results**:
- ~14 successful runs by November 28, 2025
- 14 rows in PostgreSQL `apod_data` table
- 14 entries in `include/apod_data.csv`

---

## Contributing

This is an academic project for MLOps Assignment 3. Not accepting contributions.

---

## Contact

**Student**: i221349 - Umer Abdullah
**Course**: MLOps (Semester 07)
**Institution**: [Your University Name]

---

## Acknowledgments

- **NASA APOD API**: https://api.nasa.gov
- **Astronomer**: https://www.astronomer.io
- **Neon**: https://neon.tech
- **DVC**: https://dvc.org

---

**Last Updated**: 2025-11-14
**Status**: Operational ✅
**Next Milestone**: Demo on 2025-11-28
