import os
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar']

TOKEN_PATH = './token.pickle'
CREDENTIALS_PATH = './credentials.json'


def generate_new_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_PATH,
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    with open(TOKEN_PATH, 'wb') as token:
        pickle.dump(creds, token)

    return creds


def get_credentials():
    creds = None

    ## load existing token
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    ## refresh expired token
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())

            ## save refreshed token
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        except RefreshError:
            print("Refresh token expired/revoked.")
            os.remove(TOKEN_PATH)
            creds = None

    ## no valid creds -> run OAuth flow (still working on this --connor)
    if not creds or not creds.valid:
        creds = generate_new_token()

    return creds