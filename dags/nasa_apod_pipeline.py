"""
NASA APOD Data Pipeline - Cloud Version
========================================
Optimized for Astronomer Cloud deployment.
Uses SQLite instead of PostgreSQL to avoid external database requirements.

Author: MLOps Assignment 3
"""

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import sqlite3
import os
import subprocess
from pathlib import Path

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'nasa_apod_cloud_pipeline',
    default_args=default_args,
    description='Cloud-ready ETL pipeline for NASA APOD data',
    schedule=timedelta(days=1),
    catchup=False,
    tags=['nasa', 'apod', 'etl', 'cloud'],
)


def extract_apod_data(**context):
    """Step 1: Extract data from NASA APOD API"""
    print("=" * 60)
    print("STEP 1: EXTRACTING DATA FROM NASA APOD API")
    print("=" * 60)

    api_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()

        print(f"✅ Successfully extracted data")
        print(f"   Title: {data.get('title', 'Unknown')}")
        print(f"   Date: {data.get('date', 'Unknown')}")
        print(f"   Media Type: {data.get('media_type', 'Unknown')}")

        context['task_instance'].xcom_push(key='raw_apod_data', value=data)
        return "Extraction completed"

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


def transform_apod_data(**context):
    """Step 2: Transform the raw JSON data"""
    print("=" * 60)
    print("STEP 2: TRANSFORMING DATA")
    print("=" * 60)

    raw_data = context['task_instance'].xcom_pull(
        task_ids='extract_data',
        key='raw_apod_data'
    )

    if not raw_data:
        raise ValueError("No data received from extraction")

    transformed_data = {
        'date': raw_data.get('date', ''),
        'title': raw_data.get('title', ''),
        'explanation': raw_data.get('explanation', ''),
        'url': raw_data.get('url', ''),
        'media_type': raw_data.get('media_type', ''),
        'copyright': raw_data.get('copyright', 'N/A'),
        'hdurl': raw_data.get('hdurl', ''),
    }

    df = pd.DataFrame([transformed_data])
    print(f"✅ Transformed data: {df.shape[0]} row, {df.shape[1]} columns")
    print(f"   Columns: {', '.join(df.columns.tolist())}")

    context['task_instance'].xcom_push(
        key='transformed_data',
        value=df.to_dict('records')[0]
    )
    return "Transformation completed"


def load_apod_data(**context):
    """Step 3: Load data to SQLite and CSV"""
    print("=" * 60)
    print("STEP 3: LOADING DATA")
    print("=" * 60)

    transformed_data = context['task_instance'].xcom_pull(
        task_ids='transform_data',
        key='transformed_data'
    )

    if not transformed_data:
        raise ValueError("No transformed data received")

    df = pd.DataFrame([transformed_data])

    # --- Load to SQLite Database ---
    print("📊 Loading to SQLite database...")

    airflow_home = '/usr/local/airflow'
    db_path = os.path.join(airflow_home, 'include', 'apod_data.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS apod_data (
                date TEXT PRIMARY KEY,
                title TEXT,
                explanation TEXT,
                url TEXT,
                media_type TEXT,
                copyright TEXT,
                hdurl TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert or replace
        cursor.execute("""
            INSERT OR REPLACE INTO apod_data
            (date, title, explanation, url, media_type, copyright, hdurl)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            transformed_data['date'],
            transformed_data['title'],
            transformed_data['explanation'],
            transformed_data['url'],
            transformed_data['media_type'],
            transformed_data['copyright'],
            transformed_data['hdurl']
        ))

        conn.commit()

        # Verify
        cursor.execute("SELECT COUNT(*) FROM apod_data")
        count = cursor.fetchone()[0]
        print(f"✅ SQLite: Data loaded successfully")
        print(f"   Database: {db_path}")
        print(f"   Total records: {count}")

        conn.close()

    except Exception as e:
        print(f"❌ SQLite error: {e}")
        raise

    # --- Load to CSV ---
    print("\n📄 Loading to CSV file...")

    csv_path = os.path.join(airflow_home, 'include', 'apod_data.csv')
    file_exists = os.path.exists(csv_path)

    df.to_csv(
        csv_path,
        mode='a' if file_exists else 'w',
        header=not file_exists,
        index=False
    )

    print(f"✅ CSV: Data loaded successfully")
    print(f"   File: {csv_path}")

    return "Loading completed"


def version_data_with_dvc(**context):
    """Step 4: Version the CSV file with DVC"""
    print("=" * 60)
    print("STEP 4: DVC DATA VERSIONING")
    print("=" * 60)

    airflow_home = '/usr/local/airflow'
    csv_file = 'include/apod_data.csv'
    csv_path = os.path.join(airflow_home, csv_file)

    try:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        print(f"📦 Versioning file: {csv_path}")

        # Initialize git if needed
        git_dir = os.path.join(airflow_home, '.git')
        if not os.path.exists(git_dir):
            print("   Initializing Git repository...")
            subprocess.run(['git', 'init'], cwd=airflow_home, check=True, capture_output=True)
            subprocess.run(['git', 'config', 'user.email', 'airflow@cloud.com'], cwd=airflow_home, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Airflow Cloud'], cwd=airflow_home, check=True)

        # DVC add (creates .dvc file)
        result = subprocess.run(
            ['dvc', 'add', csv_file],
            cwd=airflow_home,
            capture_output=True,
            text=True,
            check=True
        )

        print(f"✅ DVC tracking enabled")
        print(f"   Metadata file: {csv_file}.dvc")

        # Note: We skip 'dvc push' in cloud to avoid needing remote storage
        print(f"   Note: Skipping remote push (cloud environment)")

        return "DVC versioning completed"

    except subprocess.CalledProcessError as e:
        print(f"⚠️  DVC warning: {e.stderr}")
        # Don't fail - DVC is nice to have but not critical
        return "DVC versioning completed with warnings"
    except Exception as e:
        print(f"⚠️  DVC warning: {e}")
        return "DVC versioning completed with warnings"


def commit_to_git(**context):
    """Step 5: Commit the DVC metadata to Git"""
    print("=" * 60)
    print("STEP 5: GIT VERSION CONTROL")
    print("=" * 60)

    airflow_home = '/usr/local/airflow'

    try:
        # Ensure git is initialized
        git_dir = os.path.join(airflow_home, '.git')
        if not os.path.exists(git_dir):
            print("   Initializing Git repository...")
            subprocess.run(['git', 'init'], cwd=airflow_home, check=True, capture_output=True)

        # Configure git
        subprocess.run(
            ['git', 'config', 'user.email', 'airflow@cloud.com'],
            cwd=airflow_home,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ['git', 'config', 'user.name', 'Airflow Cloud'],
            cwd=airflow_home,
            check=True,
            capture_output=True
        )

        # Add files
        subprocess.run(
            ['git', 'add', 'include/'],
            cwd=airflow_home,
            capture_output=True,
            text=True
        )

        # Commit
        commit_message = f"Update APOD data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=airflow_home,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ Git commit successful")
            print(f"   Message: {commit_message}")
            return "Git commit completed"
        elif "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print(f"ℹ️  No changes to commit")
            return "No changes"
        else:
            print(f"⚠️  Git warning: {result.stderr}")
            return "Git completed with warnings"

    except Exception as e:
        print(f"⚠️  Git warning: {e}")
        return "Git completed with warnings"


# Define tasks
task_extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_apod_data,
    dag=dag,
)

task_transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_apod_data,
    dag=dag,
)

task_load = PythonOperator(
    task_id='load_data',
    python_callable=load_apod_data,
    dag=dag,
)

task_dvc_version = PythonOperator(
    task_id='version_with_dvc',
    python_callable=version_data_with_dvc,
    dag=dag,
)

task_git_commit = PythonOperator(
    task_id='commit_to_git',
    python_callable=commit_to_git,
    dag=dag,
)

# Define dependencies
task_extract >> task_transform >> task_load >> task_dvc_version >> task_git_commit
