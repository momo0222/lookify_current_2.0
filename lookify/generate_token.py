import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Path to the client_secret.json file downloaded from the Google Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIALS_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    creds = None
    # Check if token.json file exists
    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(CREDENTIALS_FILE, 'w') as token:
            token.write(creds.to_json())

    print('Access Token:', creds.token)
    print('Refresh Token:', creds.refresh_token)
    print('Client ID:', creds.client_id)
    print('Client Secret:', creds.client_secret)

if __name__ == '__main__':
    main()
