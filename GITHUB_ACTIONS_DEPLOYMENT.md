# GitHub Actions Deployment Guide

## Why GitHub Actions?

✅ **Completely Free** - No server costs
✅ **Runs 24/7** - Don't need to keep PC on
✅ **Automatic Daily Runs** - Scheduled via cron
✅ **Full History** - See every run in Actions tab
✅ **Easy Demo** - Show run history and data accumulation

---

## How It Works

We have **TWO implementations**:

### 1. **Full Airflow Pipeline** (Local/Docker)
- Location: `dags/nasa_apod_pipeline.py`
- Runs with: `astro dev start`
- Uses: PostgreSQL, DVC, full Airflow orchestration
- **For**: Demonstrations of MLOps architecture

### 2. **GitHub Actions Pipeline** (Cloud/Automated)
- Location: `scripts/standalone_pipeline.py`
- Runs: Automatically every day at 9 AM UTC
- Uses: CSV files tracked in Git
- **For**: Continuous daily data collection

Both pipelines do the same thing (Extract → Transform → Load → Version), just different execution environments.

---

## Setup (Takes 5 minutes)

### Step 1: Push to GitHub

```powershell
git remote add origin https://github.com/YOUR_USERNAME/nasa-apod-pipeline.git
git branch -M main
git push -u origin main
```

### Step 2: Enable GitHub Actions

1. Go to your GitHub repository
2. Click "Actions" tab
3. If prompted, click "I understand my workflows, go ahead and enable them"

### Step 3: Trigger First Run

**Option A: Wait for scheduled time** (9 AM UTC daily)

**Option B: Manual trigger** (recommended for testing):
1. Go to Actions tab
2. Click "NASA APOD Daily Pipeline"
3. Click "Run workflow" button
4. Select branch "main"
5. Click "Run workflow"

---

## Viewing Results

### See Run History
1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
2. Click on any run to see:
   - ✅ Success/failure status
   - 📝 Detailed logs for each step
   - ⏱️ Execution time
   - 📅 When it ran

### See Collected Data

**Latest APOD:**
`data/latest_apod.json` - Always contains today's data

**All Historical Data:**
`data/apod_data.csv` - Appends new row each day

**Run Log:**
`data/run_history.txt` - Timestamp of each successful run

### Example After 10 Days

```
data/
├── apod_data.csv          # 10 rows (one per day)
├── latest_apod.json       # Today's data
└── run_history.txt        # 10 entries
```

---

## For Your Demo (2 Weeks From Now)

### Preparation

1. **Push code today** ✅
2. **Let it run automatically** for 2 weeks
3. **Don't touch it** - GitHub Actions handles everything

### Demo Day - Part 1: Show Cloud Automation

1. **Open GitHub repository**
   ```
   https://github.com/YOUR_USERNAME/nasa-apod-pipeline
   ```

2. **Go to Actions tab**
   - Show ~14 successful runs over 2 weeks
   - Click on one to show logs
   - Prove it ran automatically

3. **Show accumulated data**
   - Open `data/apod_data.csv`
   - Show 14+ rows of data
   - Each row from different day
   - Open `data/run_history.txt`
   - Show timestamped execution log

### Demo Day - Part 2: Show Local Airflow Pipeline

1. **Clone on university laptop**
   ```bash
   git clone https://github.com/YOUR_USERNAME/nasa-apod-pipeline
   cd nasa-apod-pipeline
   ```

2. **Run full Airflow version**
   ```bash
   astro dev start
   ```

3. **Show in browser** (http://localhost:8080)
   - Full DAG with 5 tasks
   - PostgreSQL integration
   - DVC versioning
   - Professional MLOps architecture

---

## Advantages of This Dual Approach

| Feature | GitHub Actions | Airflow (Local) |
|---------|---------------|-----------------|
| **Runs automatically** | ✅ (24/7 cloud) | ⚠️ (only when PC on) |
| **Proves daily execution** | ✅ (Action history) | ⚠️ (need screenshots) |
| **Easy to demo** | ✅ (just open GitHub) | ⚠️ (need setup) |
| **MLOps architecture** | ⚠️ (simplified) | ✅ (full stack) |
| **PostgreSQL** | ❌ | ✅ |
| **DVC integration** | ⚠️ (via Git) | ✅ (full DVC) |
| **Production-like** | ⚠️ (simple) | ✅ (enterprise) |

**Best of both worlds:**
- Use **GitHub Actions** to prove it ran for 2 weeks
- Use **Airflow** to show professional architecture

---

## Troubleshooting

### Pipeline Not Running?

Check:
1. GitHub Actions is enabled (Settings → Actions → Allow all actions)
2. Workflow file is in `.github/workflows/`
3. You pushed the files to `main` branch

### Manual Trigger Not Working?

You need `workflow_dispatch` permission in the YAML (already included ✅)

### Want to Change Schedule?

Edit `.github/workflows/nasa-apod-pipeline.yml`:
```yaml
schedule:
  - cron: '0 9 * * *'  # 9 AM UTC daily
```

Change to your preferred time ([crontab.guru](https://crontab.guru) helps)

---

## Cost

💰 **$0.00** - Completely free!

GitHub Actions free tier:
- 2,000 minutes/month
- This pipeline uses ~1 minute/day
- 30 days × 1 min = 30 minutes (1.5% of quota)

---

## Summary

You now have:
1. ✅ **Local Airflow pipeline** - Full MLOps architecture with PostgreSQL, DVC, Docker
2. ✅ **GitHub Actions pipeline** - Automatic daily execution, no PC required
3. ✅ **Complete documentation** - For demo and submission

**For Demo:**
- **GitHub**: Proves it ran daily for 2 weeks (automated)
- **Airflow**: Shows professional MLOps implementation (architecture)

You get credit for both automation AND architecture! 🎉
