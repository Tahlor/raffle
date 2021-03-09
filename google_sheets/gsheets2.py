# pip install google_auth_oauthlib google-api-python-client
# https://developers.google.com/sheets/api/quickstart/python
# requests_oauthlib
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authorize(json_path='credentials_oauth2.json', token_path='token.pickle'):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                json_path, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def main(sheet_id, sheet_range, json_path, token_path):
    """ Downloads specified sheet as a nested list
    """
    creds = authorize(json_path, token_path)
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        return values

if __name__ == '__main__':
   sheet_id = '1SWz_W-PI3mZicF6kC6Iq-yHj8A1E9cecVaPsFG4wr4M'
   sheet_range = "Schedule"  # 'Class Data!A2:E'
   new_calendar = main(sheet_id, sheet_range, r"../google_sheets/credentials_oauth2.json", r"../google_sheets/token.pickle")
