import io
import pickle
import os
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaDownloadProgress, MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.appdata'
          'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.metadata','https://www.googleapis.com/auth/drive.metadata.readonly'
          'https://www.googleapis.com/auth/drive.photos.readonly','https://www.googleapis.com/auth/drive.scripts']


def get_gdrive_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    data = build('drive', 'v3', credentials=creds)
    # return Google Drive API service
    return data


dse = get_gdrive_service()


request = dse.files().export_media(fileId='file_id', mimeType='application/pdf')
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%" % int(status.progress() * 100))

# The file has been downloaded into RAM, now save it in a file
fh.seek(0)
with open('your_filename.pdf', 'wb') as f:
    shutil.copyfileobj(fh, f, length=131072)
