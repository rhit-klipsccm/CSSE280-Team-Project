import pickledb
import os

db_path = 'requests.db'
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

def add_request(request):
    db = get_db()
    db.set(
        request["name"], {
            "date": request["date"],
            "start-time": request["start-time"],
            "end-time": request["end-time"],
            "approval": "Pending"
        }
    )
    db.save()
