import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_incident_data(pid: str) -> dict:
    """Use apis for GET HAIMS Incident data by specific ID"""
    base_url = os.getenv("HAIMS_API_BASE_URL")
    url = f"{base_url}?hid={pid}"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
        
        data = response.json()

        if data and data.get("data"):
            return data
        else:
            print(f"⚠️ API response successfully but no data for ID: {pid}")
            return None
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"❌ API fail to response ID {pid}: {e}")