from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()

GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = 'credentials/client_secrets.json'

print("⏳ Going tp run Browser for Login...")
gauth.LocalWebserverAuth()

gauth.SaveCredentialsFile("credentials/mycreds.txt")
print("✅ Success! mycreds.txt file already created!")