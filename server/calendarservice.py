from googleapiclient.discovery import build
from google_auth import get_credentials
from datetime import datetime

creds = get_credentials()

service = build('calendar', 'v3', credentials=creds)

def create_event(title, start_time, end_time, description=""):
    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/Indiana/Indianapolis',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Indiana/Indianapolis',
        },
    }
    created_event = service.events().insert(
        calendarId='357fce2b791dd6d8586930ba805fc98b311249542860748111772fc4bf67f4c8@group.calendar.google.com',
        body=event
    ).execute()
    return created_event