from googleapiclient.discovery import build
from google_auth import get_credentials
from datetime import datetime
import eventservice

creds = get_credentials()

service = build('calendar', 'v3', credentials=creds)

calendar_id = '357fce2b791dd6d8586930ba805fc98b311249542860748111772fc4bf67f4c8@group.calendar.google.com'

def get_all_events():
    events = service.events().list(
        calendarId=calendar_id
    ).execute()
    return events.get("items", [])

def create_event(title, start_time, end_time, description="", color_id="5"):
    event = {
        'summary': title,
        'description': description,
        'colorId': color_id,
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
        calendarId=calendar_id,
        body=event
    ).execute()
    event_id = created_event['id']
    eventservice.add_event(event_id, created_event)
    return created_event

def patch_event(event_id, **fields):
    ## kinda stole this pattern from the first code example here: https://oneuptime.com/blog/post/2026-01-24-feature-toggles-python/view
    ## elegant (imo) way to apply fields that are passed from **fields
    updated_event_details = {}

    if fields.get("summary"):
        updated_event_details["summary"] = fields["summary"]

    if fields.get("description"):
        updated_event_details["description"] = fields["discription"]

    if fields.get("start_time"):
        updated_event_details["start"] = {
            "dateTime": datetime.strptime(fields["start_time"], "%Y-%m-%d %H:%M:%S").isoformat(),
            "timeZone": "America/Indiana/Indianapolis"
        }
    
    if fields.get("end_time"):
        updated_event_details["end"] = {
            "dateTime": datetime.strptime(fields["end_time"], "%Y-%m-%d %H:%M:%S").isoformat(),
            "timeZone": "America/Indiana/Indianapolis"
        }

    updated_event = service.events().patch(
        calendarId=calendar_id,
        eventId=event_id,
        body=updated_event_details
    ).execute()

    eventservice.patch_event(event_id, updated_event)
    return updated_event


def delete_event(event_id):
    service.events().delete(
        calendarId=calendar_id,
        eventId=event_id
    ).execute()
    eventservice.delete_event(event_id)

