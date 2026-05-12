from airflow.decorators import dag, task
from airflow.models.param import Param 
from datetime import datetime, timedelta
import os
import json  
from dotenv import load_dotenv

from includes.api_client import fetch_incident_data

load_dotenv("/opt/airflow/.env") 

LOCAL_SAVE_DIR = os.getenv("LOCAL_SAVE_DIR")

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
    tags=['haims', 'ingestion', 'bronze_layer', 'local'],
    params={
        "target_ids": Param(
            default=[
                "1110281", "1112010"
            ],
            type="array",
            description="List of Project_ID ที่ต้องการดึงข้อมูล สามารถแก้ไขได้ตอนกด Trigger"
        )
    }
)
def haims_pipeline():

    @task
    def get_target_ids(**kwargs):
        # ดึงค่าจาก Config ที่ผู้ใช้กรอกตอนกด Trigger DAG
        target_ids = kwargs['params'].get('target_ids', [])
        print(f"📋 Target IDs to process: {target_ids}")
        return target_ids

    @task(max_active_tis_per_dag=5)
    def process_single_incident(pid: str):
        print(f"🚀 Start processing ID: {pid}")
        
        incident_data = fetch_incident_data(pid)
        if not incident_data:
            return f"Skipped: {pid} (No Data)"
            
        # 1. ตรวจสอบและสร้างโฟลเดอร์ปลายทางถ้ายังไม่มี
        os.makedirs(LOCAL_SAVE_DIR, exist_ok=True)
        
        # 2. ตั้งชื่อไฟล์และสร้าง Path
        filename = f"{pid}.json"
        file_path = os.path.join(LOCAL_SAVE_DIR, filename)
        
        # 3. เขียนไฟล์ JSON ลงเครื่องโดยตรง
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(incident_data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Success: Saved {filename} locally at {file_path}")
        return pid

    ids_to_process = get_target_ids()
    process_single_incident.expand(pid=ids_to_process)

haims_bronze_layer_dag = haims_pipeline()