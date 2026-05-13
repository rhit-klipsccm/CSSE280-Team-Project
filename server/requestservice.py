import pickledb
import os
import uuid
import json

db_path = './requests.db'
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

def get_request(request_id):
    db = get_db()
    return db.get(request_id)

def get_all_requests():
    db = get_db()
    requests = {}
    for request_id in db.all():
        request_data = get_request(request_id)
        request = {
            "name": request_data["name"],
            "date": request_data["date"],
            "start-time": request_data["start_time"],
            "end-time": request_data["end_time"],
            "approval": request_data["approval"],
            "reason": request_data["reason"]
        }
        requests[request_id] = request
    return requests

def verify_entry_exists(request_id):
    if get_request(request_id) is not None:
        return True
    else:
        return False

def delete_request(request_id):
    db = get_db()
    db.remove(request_id)
    db.save()

## here, i'm aiming to allow the user to form a request_entry with the following parameters 
#  ***which must be specified***:
def form_request_entry(**fields):
    return {
        "name": fields["name"],
        "date": fields["date"],
        "start-time": fields["start_time"],
        "end-time": fields["end_time"],
        "approval": fields["approval"],
        "reason": fields["reason"]
    }


def add_request(request):
    db = get_db()
    db.set(
        uuid.uuid4(), 
        form_request_entry(
            name=request["name"],
            date=request["date"],
            ## note from connor:
            #  i don't think **kwargs supports this case: "start-time" / "end-time" / etc.
            #  current solution is to call the parameters "start_time" and "end_time", but 
            #  the fields from request object/dict. are still in their original case:
            start_time=request["start-time"],
            end_time=request["end-time"],
            ## not magical strings! requests are pending without reason by default.
            approval="Pending",
            reason=""
        )
    )
    db.save()

def patch_request(request_id, action, reason=""):
    db = get_db()
    request = get_request(request_id)
    db.set(
        request_id, 
        form_request_entry(
            name=request["name"],
            date=request["date"],
            start_time=request["start_time"],
            end_time=request["end_time"],
            approval=action,
            reason=reason
        )
    )
    db.save()



