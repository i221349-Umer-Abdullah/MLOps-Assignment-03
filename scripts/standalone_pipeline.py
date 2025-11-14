#!/usr/bin/env python3
"""
Standalone NASA APOD ETL Pipeline
For GitHub Actions - runs without Airflow/Docker
"""

import requests
import pandas as pd
import json
from datetime import datetime
import os

def extract_apod_data():
    """Step 1: Extract data from NASA APOD API"""
    print("Step 1: Extracting data from NASA APOD API...")

    api_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    response = requests.get(api_url, timeout=30)
    response.raise_for_status()
    data = response.json()

    print(f"✅ Extracted: {data.get('title', 'Unknown')}")
    return data

def transform_apod_data(raw_data):
    """Step 2: Transform the raw JSON data"""
    print("Step 2: Transforming data...")

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
    print(f"✅ Transformed: {df.shape[0]} row, {df.shape[1]} columns")
    return df

def load_apod_data(df):
    """Step 3: Load data to CSV and JSON"""
    print("Step 3: Loading data...")

    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    # Load to CSV (append mode)
    csv_path = 'data/apod_data.csv'
    file_exists = os.path.exists(csv_path)

    df.to_csv(csv_path, mode='a' if file_exists else 'w',
              header=not file_exists, index=False)

    # Also save latest as JSON for easy viewing
    latest_data = df.to_dict('records')[0]
    with open('data/latest_apod.json', 'w') as f:
        json.dump(latest_data, f, indent=2)

    # Save run log
    log_path = 'data/run_history.txt'
    with open(log_path, 'a') as f:
        f.write(f"{datetime.now().isoformat()} - SUCCESS - {latest_data['title']}\n")

    print(f"✅ Loaded to: {csv_path}")
    print(f"✅ Latest saved to: data/latest_apod.json")
    return csv_path

def version_with_dvc(csv_path):
    """Step 4: Version data with DVC (simplified for GitHub)"""
    print("Step 4: Data versioning...")

    # For GitHub Actions, we track via git commits instead of DVC
    # This is simpler and doesn't require DVC remote storage setup
    print("✅ Data will be versioned via Git commits")
    return True

def main():
    """Run the complete pipeline"""
    print("=" * 60)
    print("NASA APOD ETL Pipeline - GitHub Actions")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        # Step 1: Extract
        raw_data = extract_apod_data()

        # Step 2: Transform
        df = transform_apod_data(raw_data)

        # Step 3: Load
        csv_path = load_apod_data(df)

        # Step 4: Version
        version_with_dvc(csv_path)

        print("=" * 60)
        print("✅ Pipeline completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
