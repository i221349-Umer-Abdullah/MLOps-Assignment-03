"""
NASA APOD Data Pipeline
========================
This DAG extracts data from NASA's Astronomy Picture of the Day API,
transforms it, loads it into PostgreSQL and CSV, versions the data with DVC,
and commits the changes to Git.

Author: MLOps Assignment 3
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import psycopg2
import os
import subprocess
from pathlib import Path

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'nasa_apod_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for NASA APOD data with DVC and Git versioning',
    schedule_interval=timedelta(days=1),  # Run daily
    catchup=False,
    tags=['nasa', 'apod', 'etl', 'dvc'],
)


def extract_apod_data(**context):
    """
    Step 1: Extract data from NASA APOD API
    """
    print("Starting data extraction from NASA APOD API...")

    # NASA APOD API endpoint
    api_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()

        print(f"Successfully extracted data for: {data.get('title', 'Unknown')}")

        # Push the raw data to XCom for next task
        context['task_instance'].xcom_push(key='raw_apod_data', value=data)

        return "Data extraction completed successfully"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from NASA API: {e}")
        raise


def transform_apod_data(**context):
    """
    Step 2: Transform the raw JSON data into a clean DataFrame
    """
    print("Starting data transformation...")

    # Pull raw data from previous task
    raw_data = context['task_instance'].xcom_pull(
        task_ids='extract_data',
        key='raw_apod_data'
    )

    if not raw_data:
        raise ValueError("No data received from extraction task")

    # Select and transform specific fields
    transformed_data = {
        'date': raw_data.get('date', ''),
        'title': raw_data.get('title', ''),
        'explanation': raw_data.get('explanation', ''),
        'url': raw_data.get('url', ''),
        'media_type': raw_data.get('media_type', ''),
        'copyright': raw_data.get('copyright', 'N/A'),
        'hdurl': raw_data.get('hdurl', ''),
    }

    # Create DataFrame
    df = pd.DataFrame([transformed_data])

    print(f"Transformed data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    # Push DataFrame as dict for next task
    context['task_instance'].xcom_push(key='transformed_data', value=df.to_dict('records')[0])

    return "Data transformation completed successfully"


def load_apod_data(**context):
    """
    Step 3: Load data to PostgreSQL database and CSV file
    """
    print("Starting data loading...")

    # Pull transformed data from previous task
    transformed_data = context['task_instance'].xcom_pull(
        task_ids='transform_data',
        key='transformed_data'
    )

    if not transformed_data:
        raise ValueError("No transformed data received")

    # Create DataFrame
    df = pd.DataFrame([transformed_data])

    # --- Load to PostgreSQL ---
    print("Loading data to PostgreSQL...")

    # PostgreSQL connection parameters
    conn_params = {
        'host': 'postgres',  # Service name from docker-compose
        'port': 5432,
        'database': 'nasa_apod',
        'user': 'airflow',
        'password': 'airflow'
    }

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data (
            date DATE PRIMARY KEY,
            title TEXT,
            explanation TEXT,
            url TEXT,
            media_type VARCHAR(50),
            copyright TEXT,
            hdurl TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Insert or update data
        insert_query = """
        INSERT INTO apod_data (date, title, explanation, url, media_type, copyright, hdurl)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (date)
        DO UPDATE SET
            title = EXCLUDED.title,
            explanation = EXCLUDED.explanation,
            url = EXCLUDED.url,
            media_type = EXCLUDED.media_type,
            copyright = EXCLUDED.copyright,
            hdurl = EXCLUDED.hdurl,
            created_at = CURRENT_TIMESTAMP;
        """

        cursor.execute(insert_query, (
            transformed_data['date'],
            transformed_data['title'],
            transformed_data['explanation'],
            transformed_data['url'],
            transformed_data['media_type'],
            transformed_data['copyright'],
            transformed_data['hdurl']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Successfully loaded data to PostgreSQL")

    except Exception as e:
        print(f"Error loading data to PostgreSQL: {e}")
        raise

    # --- Load to CSV ---
    print("Loading data to CSV file...")

    # Define CSV path in the include directory (will be mounted in Docker)
    csv_path = '/usr/local/airflow/include/apod_data.csv'

    # Check if CSV exists to determine write mode
    file_exists = os.path.exists(csv_path)

    # Append to CSV or create new
    df.to_csv(
        csv_path,
        mode='a' if file_exists else 'w',
        header=not file_exists,
        index=False
    )

    print(f"Successfully loaded data to CSV: {csv_path}")

    return "Data loading completed successfully"


def version_data_with_dvc(**context):
    """
    Step 4: Version the CSV file with DVC
    """
    print("Starting DVC versioning...")

    # Change to airflow directory
    airflow_home = '/usr/local/airflow'
    csv_file = 'include/apod_data.csv'

    try:
        # Check if CSV file exists
        csv_path = os.path.join(airflow_home, csv_file)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        print(f"Versioning file: {csv_path}")

        # Add file to DVC (this creates .dvc file)
        result = subprocess.run(
            ['dvc', 'add', csv_file],
            cwd=airflow_home,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"DVC add output: {result.stdout}")

        # Push to DVC remote storage
        result = subprocess.run(
            ['dvc', 'push'],
            cwd=airflow_home,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"DVC push output: {result.stdout}")

        print("DVC versioning completed successfully")
        return "DVC versioning completed"

    except subprocess.CalledProcessError as e:
        print(f"Error running DVC command: {e}")
        print(f"Error output: {e.stderr}")
        raise
    except Exception as e:
        print(f"Error in DVC versioning: {e}")
        raise


def commit_to_git(**context):
    """
    Step 5: Commit the DVC metadata file to Git
    """
    print("Starting Git commit...")

    airflow_home = '/usr/local/airflow'

    try:
        # Configure Git user (required for commits)
        subprocess.run(
            ['git', 'config', 'user.email', 'airflow@mlops.com'],
            cwd=airflow_home,
            check=True
        )
        subprocess.run(
            ['git', 'config', 'user.name', 'Airflow Pipeline'],
            cwd=airflow_home,
            check=True
        )

        # Add the .dvc file and .gitignore to staging
        subprocess.run(
            ['git', 'add', 'include/apod_data.csv.dvc', 'include/.gitignore'],
            cwd=airflow_home,
            capture_output=True,
            text=True,
            check=True
        )

        # Create commit with timestamp
        commit_message = f"Update APOD data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=airflow_home,
            capture_output=True,
            text=True,
            check=True
        )

        print(f"Git commit completed: {commit_message}")
        return "Git commit completed"

    except subprocess.CalledProcessError as e:
        # It's okay if there's nothing to commit
        if "nothing to commit" in e.stderr or "nothing to commit" in e.stdout:
            print("No changes to commit")
            return "No changes to commit"
        print(f"Error running Git command: {e}")
        print(f"Error output: {e.stderr}")
        raise
    except Exception as e:
        print(f"Error in Git commit: {e}")
        raise


# Define tasks
task_extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_apod_data,
    provide_context=True,
    dag=dag,
)

task_transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_apod_data,
    provide_context=True,
    dag=dag,
)

task_load = PythonOperator(
    task_id='load_data',
    python_callable=load_apod_data,
    provide_context=True,
    dag=dag,
)

task_dvc_version = PythonOperator(
    task_id='version_with_dvc',
    python_callable=version_data_with_dvc,
    provide_context=True,
    dag=dag,
)

task_git_commit = PythonOperator(
    task_id='commit_to_git',
    python_callable=commit_to_git,
    provide_context=True,
    dag=dag,
)

# Define task dependencies (sequential pipeline)
task_extract >> task_transform >> task_load >> task_dvc_version >> task_git_commit
