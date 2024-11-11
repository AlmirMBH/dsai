from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates a local webserver and automatically handles authentication
drive = GoogleDrive(gauth)

# Create a directory to store the downloaded files
os.makedirs('MyDrive', exist_ok=True)

# List files in your Google Drive
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in file_list:
    print(f'Title: {file["title"]}, ID: {file["id"]}')

# To download a specific file, use its ID
file_id = 'your_file_id_here'  # Replace with the ID of the file you want to download
downloaded_file = drive.CreateFile({'id': file_id})
downloaded_file.GetContentFile('MyDrive/your_file_name.csv')  # Save the file to the MyDrive folder
