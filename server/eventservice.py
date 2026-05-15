import pickledb
import os
import uuid
import json

db_path = './events.db'
global_db = None

def load_db():
    global global_db
    db_file_already_exists = os.path.exists(db_path)
    global_db = pickledb.PickleDB(db_path)
    if not db_file_already_exists:
        global_db.save()

def get_db():
    global global_db
    if global_db is None:
        load_db()
    return global_db

def get_event(event_id):
    db = get_db()
    return db.get(event_id)

def get_all_event_ids():
    db = get_db()
    return db.all()


def add_event(event_id, google_event):
    db = get_db()
    ## if i had a time machine, i would have structured the data this way... WAY beforehand

    event = {
        "google_event_id": event_id,
        "title": google_event.get("summary", ""),
        "description": google_event.get("description", ""),
        "start": {
            "datetime": google_event["start"].get("dateTime"),
            "timezone": google_event["start"].get("timeZone"),
        },
        "end": {
            "datetime": google_event["end"].get("dateTime"),
            "timezone": google_event["end"].get("timeZone"),
        },
        "created": google_event.get("created"),
        "updated": google_event.get("updated"),
        "status": google_event.get("status"),
        "html_link": google_event.get("htmlLink"),
    }
    db.set(event_id, event)
    db.save()

def patch_event(event_id, updated_details):
    db = get_db()
    event = get_event(event_id)
    for field in updated_details:
        if updated_details[field] != '' and field in event:
            event[field] = updated_details[field]
    db.set(
        event_id,
        event
    )
    db.save()
    return

def delete_event(event_id):
    db = get_db()
    db.remove(event_id)
    db.save()
