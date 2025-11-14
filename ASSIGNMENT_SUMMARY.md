# NASA APOD ETL Pipeline - Assignment Summary

## What We Built

A complete MLOps data pipeline that automatically fetches NASA's Astronomy Picture of the Day, processes it, stores it in multiple formats, and versions everything for reproducibility.

---

## The 5-Step Pipeline

### Step 1: Extract Data
- Connects to NASA's APOD API (https://api.nasa.gov/planetary/apod)
- Fetches today's astronomy picture data in JSON format
- Includes: date, title, explanation, image URL, copyright, etc.

### Step 2: Transform Data
- Selects relevant fields from the raw JSON
- Cleans and structures data using Pandas DataFrame
- Prepares data for storage in a consistent format

### Step 3: Load Data (Dual Storage)
**PostgreSQL Database:**
- Creates table `apod_data` if it doesn't exist
- Stores data with primary key on date
- Handles updates automatically (upsert operation)

**CSV File:**
- Saves data to `include/apod_data.csv`
- Appends new data each run
- Easy to share and analyze

### Step 4: Version Data with DVC
- Uses Data Version Control (DVC) to track the CSV file
- Creates `apod_data.csv.dvc` metadata file
- Pushes actual data to local DVC storage
- Ensures data reproducibility

### Step 5: Commit to Git
- Commits the DVC metadata file to Git
- Links code version to data version
- Enables full pipeline reproducibility

---

## Technologies Used

1. **Apache Airflow** - Workflow orchestration
2. **Astronomer** - Airflow deployment platform (Docker-based)
3. **PostgreSQL** - Relational database for structured data
4. **DVC (Data Version Control)** - Data versioning and tracking
5. **Git/GitHub** - Code version control
6. **Docker** - Containerization for all services
7. **Python** - Pipeline implementation language
8. **Pandas** - Data transformation
9. **psycopg2** - PostgreSQL database adapter

---

## How to Run

### Prerequisites
- Docker Desktop installed and running
- Astronomer CLI installed (`winget install -e --id Astronomer.Astro`)
- Git installed

### Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Assignment 03"
   ```

2. **Start the Airflow environment**
   ```powershell
   astro dev start
   ```
   This starts:
   - Airflow webserver (http://localhost:8080)
   - Airflow scheduler
   - PostgreSQL database
   - All supporting services

3. **Access Airflow UI**
   - Open browser to http://localhost:8080
   - Login: admin / admin
   - Find DAG: `nasa_apod_etl_pipeline`
   - Toggle it ON to enable
   - Click "Trigger" to run manually

4. **View the pipeline execution**
   - Watch tasks turn green as they complete
   - Check logs for each task
   - Verify all 5 tasks succeed

5. **Stop the environment**
   ```powershell
   astro dev stop
   ```

---

## Project Structure

```
Assignment 03/
├── dags/
│   └── nasa_apod_pipeline.py      # Main Airflow DAG (5 tasks)
├── include/
│   ├── apod_data.csv              # Loaded data (tracked by DVC)
│   └── apod_data.csv.dvc          # DVC metadata file
├── .dvc/
│   └── config                     # DVC configuration
├── dvc-storage/                   # Local DVC remote storage
├── docker-compose.override.yml    # PostgreSQL container config
├── requirements.txt               # Python dependencies
├── packages.txt                   # System packages (git)
├── Dockerfile                     # Docker image config
├── ISSUES_AND_FIXES.md           # Problem-solving documentation
└── ASSIGNMENT_SUMMARY.md          # This file
```

---

## Key Features

✅ **Automated ETL Pipeline** - Runs daily automatically or on-demand
✅ **Dual Persistence** - Data in both PostgreSQL and CSV formats
✅ **Data Versioning** - DVC tracks all data changes
✅ **Code Versioning** - Git tracks all code changes
✅ **Reproducible** - Anyone can recreate exact results
✅ **Containerized** - Runs consistently across all environments
✅ **Production-Ready** - Uses industry-standard MLOps tools

---

## Verification

### Check PostgreSQL Data
```bash
docker exec nasa-apod-postgres psql -U airflow -d nasa_apod -c "SELECT * FROM apod_data;"
```

### Check CSV File
```bash
docker exec assignment-03_8c6823-scheduler-1 cat /usr/local/airflow/include/apod_data.csv
```

### Check DVC Tracking
```bash
docker exec assignment-03_8c6823-scheduler-1 cat /usr/local/airflow/include/apod_data.csv.dvc
```

---

## What We Learned

1. **Workflow Orchestration**: How to define complex, dependent tasks using Airflow DAGs
2. **Data Integrity**: Techniques for loading data to multiple destinations simultaneously
3. **Data Lineage**: Using DVC with Git for complete data and code versioning
4. **Containerization**: Building custom Docker images with all necessary dependencies
5. **MLOps Best Practices**: Reproducible pipelines, version control, and automation

---

## Assignment Requirements Met

| Requirement | Status | Evidence |
|------------|--------|----------|
| Extract from NASA API | ✅ | `extract_data` task succeeds |
| Transform JSON data | ✅ | `transform_data` task succeeds |
| Load to PostgreSQL | ✅ | Data queryable in `apod_data` table |
| Load to CSV | ✅ | `apod_data.csv` file created |
| DVC versioning | ✅ | `.dvc` file generated and data tracked |
| Git versioning | ✅ | DVC metadata committed |
| Airflow orchestration | ✅ | All tasks in sequential DAG |
| Docker deployment | ✅ | Running via Astronomer/Docker |
| Reproducibility | ✅ | DVC + Git ensure repeatability |

---

## Issues Encountered and Resolved

See [ISSUES_AND_FIXES.md](ISSUES_AND_FIXES.md) for detailed documentation of all 10 issues encountered during development and how they were resolved.

Key challenges:
- Airflow 3.x API changes (deprecated parameters)
- Docker network configuration
- PostgreSQL container networking
- DVC requiring Git repository
- Port conflicts

All issues successfully resolved with working solutions documented.

---

## Author
MLOps Assignment 3 - November 2025

## Acknowledgments
- NASA APOD API for providing astronomy data
- Apache Airflow community
- Astronomer for deployment tools
- DVC team for data versioning solution
