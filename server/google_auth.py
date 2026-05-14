import os
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_credentials():

    creds = None

    if os.path.exists('./token.pickle'):
        with open('./token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds:
        raise Exception(
            "No credentials found. Run OAuth locally first and copy token.pickle to server. -connor"
        )

    return creds