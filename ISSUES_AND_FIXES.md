# NASA APOD ETL Pipeline - Issues and Fixes Log

This document tracks all problems encountered during the MLOps Assignment 3 project and their solutions.

---

## Issue 1: Python Package Version Conflict
**File**: `requirements.txt`
**Problem**: Airflow 3.1.2 requires `requests>=2.32.0`, but we initially specified `requests==2.31.0`
**Error Message**:
```
Because apache-airflow-core==3.1.2+astro.1 depends on requests>=2.32.0
and you require requests==2.31.0, your requirements are unsatisfiable.
```
**Fix**: Changed `requests==2.31.0` to `requests>=2.32.0` in requirements.txt
**Status**: ✅ RESOLVED

---

## Issue 2: Docker Network Configuration Conflict
**File**: `docker-compose.override.yml`
**Problem**: Service named "postgres" conflicted with Astronomer's internal postgres service, and network declared as external but didn't exist
**Error Message**:
```
network airflow declared as external, but could not be found
```
**Fix**:
- Removed `version` field (obsolete in Docker Compose v2)
- Removed `networks` section (let Docker handle networking automatically)
- Renamed service from `postgres` to `nasa-postgres` to avoid naming conflicts
- Kept container name as `nasa-apod-postgres` for connection consistency
**Status**: ✅ RESOLVED

---

## Issue 3: Port 5432 Already in Use
**File**: `docker-compose.override.yml`
**Problem**: Port 5432 was already bound by another PostgreSQL instance or Airflow's metadata database
**Error Message**:
```
failed to listen on TCP socket: address already in use
```
**Fix**: Changed external port mapping from `5432:5432` to `5433:5432`
**Note**: Internal port remains 5432, only host access is via port 5433
**Status**: ✅ RESOLVED

---

## Issue 4: Deprecated Airflow 3.x Parameter - schedule_interval
**File**: `dags/nasa_apod_pipeline.py` (line 37)
**Problem**: Airflow 3.x deprecated `schedule_interval` parameter in favor of `schedule`
**Error Message**:
```
TypeError: DAG.__init__() got an unexpected keyword argument 'schedule_interval'
```
**Fix**: Changed `schedule_interval=timedelta(days=1)` to `schedule=timedelta(days=1)`
**Status**: ✅ RESOLVED

---

## Issue 5: Deprecated PythonOperator Import Path
**File**: `dags/nasa_apod_pipeline.py` (line 12)
**Problem**: Import path `airflow.operators.python.PythonOperator` is deprecated in Airflow 3.x
**Warning Message**:
```
DeprecatedImportWarning: The `airflow.operators.python.PythonOperator` attribute is deprecated.
Please use 'airflow.providers.standard.operators.python.PythonOperator'
```
**Fix**: Changed import from `from airflow.operators.python import PythonOperator` to `from airflow.providers.standard.operators.python import PythonOperator`
**Status**: ✅ RESOLVED

---

## Issue 6: Deprecated provide_context Parameter
**File**: `dags/nasa_apod_pipeline.py` (lines 322-350)
**Problem**: Airflow 3.x automatically provides context to PythonOperator callables; `provide_context=True` parameter is invalid
**Error Message**:
```
TypeError: Invalid arguments were passed to PythonOperator (task_id: extract_data).
Invalid arguments were: **kwargs: {'provide_context': True}
```
**Fix**: Removed `provide_context=True` from all 5 PythonOperator definitions
**Files Changed**: All task definitions (task_extract, task_transform, task_load, task_dvc_version, task_git_commit)
**Status**: ✅ RESOLVED

---

## Issue 7: PostgreSQL Connection Host Configuration
**File**: `dags/nasa_apod_pipeline.py` (line 130)
**Problem**: Initially used generic service name 'postgres', needed to match actual container name
**Fix**: Updated host from `'postgres'` to `'nasa-apod-postgres'` to match container_name in docker-compose
**Status**: ✅ RESOLVED

---

## Issue 8: Docker Disk Space
**Problem**: Docker had 4GB/5.7GB space occupied with old images and build cache
**Fix**:
- Ran `docker system prune -a --filter "until=720h" -f` - freed 452MB
- Ran `docker builder prune -af` - freed 3.2GB
- **Total space recovered**: 3.7GB
**Status**: ✅ RESOLVED

---

## Issue 9: Docker Network Isolation
**File**: `docker-compose.override.yml`
**Problem**: PostgreSQL container was on `assignment-03_8c6823_default` network while Airflow containers were on `assignment-03_8c6823_airflow` network
**Error Message**:
```
could not translate host name "nasa-apod-postgres" to address: Name or service not known
```
**Fix**: Added network configuration to docker-compose.override.yml to connect nasa-postgres service to the airflow network
```yaml
networks:
  - airflow

networks:
  airflow:
    name: assignment-03_8c6823_airflow
    external: true
```
**Status**: ✅ RESOLVED

---

## Issue 10: Git Repository Not Available in Container
**File**: `dags/nasa_apod_pipeline.py` (lines 233-240, 283-287)
**Problem**: `/usr/local/airflow` inside Docker container is not a git repository; Astronomer doesn't mount the `.git` folder
**Error Message**:
```
ERROR: /usr/local/airflow is not a git repository
```
**Fix**: Modified DVC and Git tasks to initialize git repository inside container if it doesn't exist:
```python
if not os.path.exists(git_dir):
    subprocess.run(['git', 'init'], cwd=airflow_home, check=True, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'airflow@mlops.com'], cwd=airflow_home, check=True)
    subprocess.run(['git', 'config', 'user.name', 'Airflow Pipeline'], cwd=airflow_home, check=True)
```
**Status**: ✅ RESOLVED

---

## Issue 11: Cloud Deployment Architecture Decision - SQLite vs PostgreSQL
**Context**: Assignment requires PostgreSQL, but initial cloud deployment used SQLite
**Problem**: After successful local deployment with PostgreSQL, switched to SQLite for cloud to avoid external database management
**User Feedback**: "we cant use sqlite, will have to use postgreSQL... we will try to follow assignment as hardly as possible"
**Decision Process**:
1. Researched cloud PostgreSQL options (free tier requirement)
2. Evaluated Neon PostgreSQL serverless database:
   - Free tier: 0.5GB storage, 100 compute hours/month
   - Auto-suspend after 5 min inactivity (500ms cold start)
   - Completely cloud-based, no local PC required
   - No credit card required
3. User approved: "yes" to proceed with Neon setup

**Fix**: Migrated from SQLite to Neon PostgreSQL
- Updated [dags/nasa_apod_pipeline.py](dags/nasa_apod_pipeline.py:15) - Changed import from `sqlite3` to `psycopg2`
- Updated [dags/nasa_apod_pipeline.py](dags/nasa_apod_pipeline.py:103-187) - Replaced SQLite connection with PostgreSQL connection using environment variable `NEON_DB_CONN_STRING`
- Updated [requirements.txt](requirements.txt:8) - Added `psycopg2-binary==2.9.9`
- Configured Astronomer environment variable for secure connection string storage
- Redeployed to Astronomer Cloud
**Status**: ✅ RESOLVED

---

## Issue 12: GitHub Token Workflow Scope
**File**: `.github/workflows/nasa-apod-pipeline.yml`
**Problem**: Personal Access Token lacked `workflow` scope to push GitHub Actions workflow files
**Error Message**:
```
! [remote rejected] main -> main (refusing to allow a Personal Access Token to create or update workflow `.github/workflows/nasa-apod-pipeline.yml` without `workflow` scope)
```
**Fix**: Removed `.github/workflows/` directory since using Astronomer Cloud for deployment (GitHub Actions workflow not needed)
**Status**: ✅ RESOLVED

---

## Summary of All File Changes

### 1. requirements.txt
- Changed: `requests==2.31.0` → `requests>=2.32.0`
- Added: `psycopg2-binary==2.9.9` (for Neon PostgreSQL)

### 2. docker-compose.override.yml
- Removed: `version: "3.1"`
- Renamed: service `postgres` → `nasa-postgres`
- Changed: port `5432:5432` → `5433:5432`
- Removed: `networks` section
- Renamed: volume `postgres-data` → `nasa-postgres-data`
- **Note**: Used for local development only; cloud deployment uses Neon PostgreSQL

### 3. dags/nasa_apod_pipeline.py
- Changed: Import path for PythonOperator to new Airflow 3.x path
- Changed: `schedule_interval` → `schedule`
- Removed: `provide_context=True` from all 5 PythonOperator instances
- Updated: PostgreSQL host to `nasa-apod-postgres` (local)
- **Cloud Version Changes**:
  - Changed: `import sqlite3` → `import psycopg2`
  - Changed: Load function to use Neon PostgreSQL with environment variable
  - Changed: Connection string from hardcoded to `os.getenv('NEON_DB_CONN_STRING')`

### 4. packages.txt
- Added: `git` (required for Git operations in Step 5)

### 5. .gitignore
- Added: `dvc-storage/` directory

### 6. .github/workflows/
- Removed: Entire directory (using Astronomer Cloud instead of GitHub Actions)

---

## Key Learnings

1. **Airflow 3.x Breaking Changes**: Multiple parameters and import paths changed from Airflow 2.x
2. **Docker Networking**: Astronomer manages its own network; custom services should not declare external networks
3. **Port Conflicts**: Always check for port availability before binding container ports
4. **Version Compatibility**: Always check dependency version requirements when using specific framework versions
5. **Container Naming**: Use unique container/service names to avoid conflicts with framework-managed services

---

## Final Configuration

### Working Setup:
- **Airflow Version**: 3.1.2+astro.1 (Astronomer Runtime 3.1-4)
- **Python Version**: 3.12
- **PostgreSQL Version**: Neon PostgreSQL (Serverless, Cloud-based)
- **DVC Version**: 3.64.0
- **Pandas Version**: 2.2.0
- **Requests Version**: >=2.32.0
- **psycopg2-binary Version**: 2.9.9

### Cloud Deployment Architecture:
```
Astronomer Cloud (AWS ap-southeast-1)
├── Airflow UI: https://cmhyv36ur0viz01kawg1ffecd.astronomer.run/dizdq47g
├── Deployment ID: cmhyv4tge0vjj01ka2izdq47g
└── Environment Variables: NEON_DB_CONN_STRING (secret)

Neon PostgreSQL (Cloud)
├── Region: ap-southeast-1
├── Database: neondb
└── Table: apod_data (auto-created by pipeline)

GitHub Repository
└── https://github.com/i221349-Umer-Abdullah/MLOps-Assignment-03
```

### Local Development Architecture (Optional):
```
Airflow Containers (Astronomer-managed):
├── api-server (port 8080)
├── scheduler
├── triggerer
├── dag-processor
└── postgres (Airflow metadata)

Custom Containers:
└── nasa-apod-postgres (port 5433→5432)
```

### Deployment Timeline:
1. **2025-11-14**: Initial local development with PostgreSQL
2. **2025-11-14**: First cloud deployment with SQLite
3. **2025-11-14**: Final cloud deployment with Neon PostgreSQL
4. **2025-11-14**: Code pushed to GitHub

---

**Report Generated**: 2025-11-14
**Project**: MLOps Assignment 3 - NASA APOD Data Pipeline
**Status**: ✅ All issues resolved, pipeline operational in cloud
**Next Milestone**: Monitor automated daily runs for 2 weeks (until 2025-11-28)
