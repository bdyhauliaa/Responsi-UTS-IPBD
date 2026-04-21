from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# supaya airflow bisa akses folder app
sys.path.append('/opt/airflow/app')

def scrape():
    os.system("python app/scraper/wired_scraper.py")

def transform():
    os.system("python app/pipeline/transform.py")

def load():
    os.system("python -m app.pipeline.load_to_db")

with DAG(
    dag_id="wired_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    task_scrape = PythonOperator(
        task_id="scrape_data",
        python_callable=scrape
    )

    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform
    )

    task_load = PythonOperator(
        task_id="load_to_db",
        python_callable=load
    )

    task_scrape >> task_transform >> task_load