# Demo Preparation Guide

## Screenshots to Take NOW (Before Demo)

### 1. Airflow UI - DAG Overview
- URL: http://localhost:8080
- Capture: Main dashboard showing the `nasa_apod_etl_pipeline`
- Show: DAG is active and scheduled to run daily

### 2. Successful Run - All Tasks Green
- Navigate to the DAG detail page
- Capture: Graph view with all 5 tasks green (successful)
- Show timestamps of execution

### 3. Task Logs
Take screenshots of logs for each task:
- **extract_data**: Show API call and data retrieval
- **transform_data**: Show DataFrame creation
- **load_data**: Show PostgreSQL insertion and CSV creation
- **version_with_dvc**: Show DVC tracking
- **commit_to_git**: Show git commit message

### 4. PostgreSQL Data
```bash
docker exec nasa-apod-postgres psql -U airflow -d nasa_apod -c "SELECT * FROM apod_data;"
```
Capture the query results showing stored data

### 5. CSV File Content
```bash
docker exec assignment-03_8c6823-scheduler-1 cat /usr/local/airflow/include/apod_data.csv
```
Capture the CSV data

### 6. DVC Files
```bash
docker exec assignment-03_8c6823-scheduler-1 ls -la /usr/local/airflow/include/
```
Show `.dvc` file exists

### 7. Multiple Run History
Wait a few days, let it run 3-5 times, then capture:
- DAG Runs page showing multiple successful executions
- Calendar view showing runs on different dates
- PostgreSQL table with multiple rows from different dates

---

## For the Demo Day (University Laptop)

### Setup Instructions (10-15 minutes)

1. **Clone Repository**
   ```bash
   git clone <your-github-url>
   cd "Assignment 03"
   ```

2. **Ensure Prerequisites**
   - Docker Desktop installed
   - Astronomer CLI installed: `winget install -e --id Astronomer.Astro`

3. **Start Environment**
   ```powershell
   astro dev start
   ```
   Wait 3-5 minutes for services to start

4. **Access Airflow**
   - Open http://localhost:8080
   - Login: admin / admin
   - Enable the DAG
   - Trigger a manual run

### What to Show

#### Part 1: Code Walkthrough (5 min)
1. Open `dags/nasa_apod_pipeline.py` in VS Code
2. Explain the 5 tasks
3. Show how tasks are connected: `task1 >> task2 >> task3...`

#### Part 2: Live Demo (10 min)
1. **Show Airflow UI**
   - Explain DAG structure
   - Show graph view
   - Trigger manual run

2. **Watch Execution**
   - Tasks turn green one by one
   - Show live logs for each task

3. **Verify Outputs**

   **PostgreSQL:**
   ```bash
   docker exec nasa-apod-postgres psql -U airflow -d nasa_apod -c "SELECT date, title FROM apod_data;"
   ```

   **CSV File:**
   ```bash
   docker exec assignment-03_8c6823-scheduler-1 cat /usr/local/airflow/include/apod_data.csv
   ```

   **DVC Tracking:**
   ```bash
   docker exec assignment-03_8c6823-scheduler-1 cat /usr/local/airflow/include/apod_data.csv.dvc
   ```

#### Part 3: Show Historical Runs (5 min)
- **Option A**: Show screenshots from 2-week period
- **Option B**: Show GitHub commit history
- **Option C**: If you kept it running, show Airflow's run history

#### Part 4: Architecture Explanation (5 min)
- Explain Docker containers
- Show docker-compose.override.yml
- Explain DVC for data versioning
- Explain why this is MLOps

---

## Alternative: Cloud Deployment (OPTIONAL - Advanced)

If you want to show it running continuously without keeping your PC on:

### Free Cloud Options

**1. Astronomer Cloud (Free Trial)**
- Sign up at https://www.astronomer.io/
- Deploy your project: `astro deploy`
- Runs 24/7 in the cloud
- Free tier available

**2. GitHub Actions + DVC**
- Use GitHub Actions to run the pipeline on schedule
- Store data in GitHub (or cloud storage)
- Completely free

**Would you like me to help set this up?**

---

## My Recommendation for YOU

**For 2-week preparation:**

1. **Take screenshots TODAY** (all 7 listed above)

2. **Let it run for 3-5 days** (not full 2 weeks needed)
   - Collect screenshots showing multiple runs
   - Take screenshots every 2-3 days

3. **For the Demo:**
   - Prepare a **PowerPoint/PDF** with screenshots showing:
     - Initial setup
     - Multiple successful runs over time
     - Data accumulation in PostgreSQL
     - DVC tracking working
   - Do a **LIVE demo** on university laptop:
     - Fresh install from GitHub
     - Run it once live
     - Show all 5 tasks succeeding
     - Query PostgreSQL and show CSV

4. **Backup Plan:**
   - If live demo fails, you have screenshots
   - If time is short, screenshots prove it worked

**This approach:**
- ✅ Proves it ran multiple times (screenshots)
- ✅ Shows you can deploy anywhere (live on laptop)
- ✅ Demonstrates reproducibility (GitHub to fresh install)
- ✅ Doesn't require keeping PC on for 2 weeks
- ✅ No cloud deployment needed (saves complexity)

---

## Quick Demo Script

**Opening (30 sec):**
"I built an MLOps pipeline that automatically fetches NASA's astronomy data daily, processes it, stores it in PostgreSQL and CSV, and versions everything with DVC and Git."

**Screenshots (2 min):**
"Here are screenshots showing it ran successfully over the past 2 weeks [show slides]"

**Live Demo (5-10 min):**
"Let me show you it working live. I'll clone from GitHub and run it fresh..."
[Do the setup and run it]

**Verification (2 min):**
"Now let's verify the outputs..."
[Show PostgreSQL query, CSV file, DVC tracking]

**Architecture (2 min):**
"The architecture uses Docker containers for Airflow and PostgreSQL, DVC for data versioning, and Git for code versioning..."

**Total: 10-15 minutes**

---

## Files Included for Demo

- ✅ ASSIGNMENT_SUMMARY.md - Overview
- ✅ ISSUES_AND_FIXES.md - Problem-solving documentation
- ✅ README.md - Setup instructions
- ✅ This file - Demo preparation guide

