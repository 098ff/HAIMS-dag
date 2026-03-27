from airflow.decorators import dag, task
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from includes.api_client import fetch_incident_data
from includes.gdrive_client import get_gdrive_client, upload_json_to_gdrive

load_dotenv("/opt/airflow/.env") 

GDRIVE_FOLDER_ID = os.getenv("GDRIVE_TARGET_FOLDER_ID")
CREDS_PATH = os.getenv("CREDS_PATH")
CLIENT_SECRETS_PATH = os.getenv("CLIENT_SECRETS_PATH")

default_args = {
    'owner': 'fforfaii',
    'depends_on_past': False,
    'retries': 2, 
    'retry_delay': timedelta(minutes=1),
}

@dag(
    dag_id='haims_bronze_layer_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2026, 3, 26),
    catchup=False,
    tags=['haims', 'ingestion', 'bronze_layer'],
)
def haims_pipeline():

    @task
    def get_target_ids():
        start_id = 1161550
        stop_id = 1161559
        return [str(i) for i in range(start_id, stop_id + 1)]

    @task(max_active_tis_per_dag=5)
    def process_single_incident(pid: str):
        print(f"🚀 Start processing ID: {pid}")
        
        incident_data = fetch_incident_data(pid)
        if not incident_data:
            return f"Skipped: {pid} (No Data)"
            
        drive = get_gdrive_client(CREDS_PATH, CLIENT_SECRETS_PATH)
        
        filename = f"{pid}.json"
        upload_json_to_gdrive(drive, GDRIVE_FOLDER_ID, filename, incident_data)
        
        print(f"✅ Success: upload {filename} successfully")
        return pid

    ids_to_process = get_target_ids()
    process_single_incident.expand(pid=ids_to_process)

haims_bronze_layer_dag = haims_pipeline()