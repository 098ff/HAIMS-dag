from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json

def get_gdrive_client(creds_path: str, client_secrets_path: str) -> GoogleDrive:
    gauth = GoogleAuth()
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_path
    
    gauth.LoadCredentialsFile(creds_path)
    
    if gauth.credentials is None or gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(creds_path)
        
    return GoogleDrive(gauth)

def upload_json_to_gdrive(drive: GoogleDrive, folder_id: str, filename: str, json_data: dict) -> str:
    json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
    file_metadata = {
        'title': filename,
        'parents': [{'id': folder_id}],
        'mimeType': 'application/json'
    }
    
    file_drive = drive.CreateFile(file_metadata)
    file_drive.SetContentString(json_str)
    file_drive.Upload()
    
    return file_drive['id']