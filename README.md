# ⚙️ HAIMS Bronze Layer Ingestion Pipeline

This repository contains an automated Data Engineering pipeline powered by **Apache Airflow** and **Docker**. It extracts highway accident data from the HAIMS API and loads it directly into Google Drive as JSON files (Bronze Layer), utilizing concurrent processing and GCP Service Account authentication.

---

## 🌟 Key Features
- **Fully Automated Orchestration:** Scheduled and monitored using Apache Airflow.
- **Concurrent API Extraction:** Uses Airflow's Dynamic Task Mapping (`.expand()`) to fetch multiple incident reports in parallel, significantly reducing processing time.
- **Enterprise-Grade Authentication:** Employs Google Cloud Platform (GCP) Service Accounts for headless, token-free, and permanent authentication to Google Drive.
- **Modular Architecture:** Clean separation of concerns between DAG definitions, API clients, and Google Drive services.

---

## 📂 Directory Structure

```text
dag_haims/
├── dags/
│   ├── haims_api_to_gdrive_dag.py    # Main Airflow DAG orchestrator
│   └── includes/                     # Business logic modules
│       ├── __init__.py
│       ├── api_client.py             # HAIMS API extraction logic
│       └── gdrive_client.py          # Google Drive upload logic using GCP Service Account
├── credentials/                      # 🔐 Ignored by Git
│   └── sa_secrets.json               # GCP Service Account Key
├── logs/                             # Airflow execution logs
├── plugins/                          # Airflow plugins (if any)
├── docker-compose.yaml               # Airflow Docker configuration
└── .env                              # Environment variables
```

---

## 🛠️ Prerequisites

Before running the pipeline, ensure you have the following installed on your local machine or server:
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- A **GCP Service Account Key** (`.json`) with "Editor" access to the target Google Drive folder.

---

## ⚙️ Configuration & Setup

### 1. Environment Variables (`.env`)
Create a `.env` file in the root of `dag_haims/` and configure the following parameters:

```env
# Airflow Docker Settings
AIRFLOW_UID=50000
_PIP_ADDITIONAL_REQUIREMENTS=google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv requests

# HAIMS API Configuration
HAIMS_API_BASE_URL="[https://haims2.doh.go.th/get/case_data](https://haims2.doh.go.th/get/case_data)"

# Google Drive Target
GDRIVE_TARGET_FOLDER_ID="your_google_drive_folder_id_here"

# GCP Service Account Path (Internal Docker path)
GCP_SA_KEY_PATH="/opt/airflow/credentials/your_service_account_key_name_here.json"
```

### 2. Credentials
Place your downloaded GCP Service Account key inside the `credentials/` folder and rename it to exactly match your `.env` configuration.

> ⚠️ **SECURITY WARNING:** Never commit the `credentials/` folder or the `.env` file to version control. They are included in `.gitignore`.

---

## 🚀 How to Run

### Step 1: Initialize Airflow Database
Run the following command to set up the Airflow metadata database. **This only needs to be done once:**
```bash
docker compose up airflow-init
```
*(Wait until you see the message `exited with code 0`)*

### Step 2: Start the Pipeline Services
Start all Airflow components (Webserver, Scheduler, Worker) in detached mode:
```bash
docker compose up -d
```

### Step 3: Access Airflow UI
1. Open your web browser and navigate to: `http://localhost:8080`
2. **Username:** `airflow`
3. **Password:** `airflow`
4. Locate the DAG named `haims_bronze_layer_pipeline`.
5. Unpause the DAG (toggle the blue switch) and click the **Trigger (▶️)** button to start the ingestion process.

---

## 🛑 Stopping the Services
To stop the Airflow containers and free up system resources, run:
```bash
docker compose down
```
*(Note: Use `docker compose down --volumes` if you want to completely wipe the Airflow database and start fresh).*
