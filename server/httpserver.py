import flask
import json
import requestservice
import calendarservice
import os
from flask import request
from datetime import datetime

from werkzeug.utils import secure_filename

app = flask.Flask(__name__,
            static_url_path='',
            static_folder='dist')


@app.get("/shutdown")
def shutdown():
    os._exit(0)

@app.get("/requests")
def get_requests():
    requests = requestservice.get_all_requests()
    return flask.Response(
        status="200 OK",
        headers={"Content-Type": "application/json"},
        response=json.dumps(requests)
    )

@app.post("/requests")
def submit_request():
    data = flask.request.form
    event_id = calendarservice.create_event(
        data["name"],
        start_time=datetime.strptime(" ".join([data["date"], data["start-time"]]), "%Y-%m-%d %H:%M"),
        end_time=datetime.strptime(" ".join([data["date"], data["end-time"]]), "%Y-%m-%d %H:%M"),
        description="¡PENDING!"
    )
    requestservice.add_request(data, event_id)
    return flask.redirect("/index.html")

@app.patch("/requests/<request_id>")
def update_request(request_id):
    data = request.get_json()
    
    ## TODO: Implement the following fields on the admin page:
    approval_action = data.get("action")
    reason = data.get("reason")

    requestservice.patch_request(request_id, approval_action, reason)
    return flask.redirect("/admin.html")

@app.delete("/requests/<request_id>")
def delete_request(request_id):
    if requestservice.verify_entry_exists(request_id):
        requestservice.delete_request(request_id)
    return flask.redirect("/admin.html")


## /events endpoints now:
@app.delete("/events/<event_id>")
def delete_event(event_id):
    calendarservice.delete_event(event_id)
    return flask.Response(
        status="200 OK",
        response="Deleted!"
    )

@app.post("/events")
def create_event():
    data = request.get_json()
    created_event = calendarservice.create_event(
        title=data["title"],
        start_time=datetime.strptime(" ".join([data["date"], data["start-time"]]), "%Y-%m-%d %H:%M"),
        end_time=datetime.strptime(" ".join([data["date"], data["start-time"]]), "%Y-%m-%d %H:%M"),
        description=data.get("description", "")
    )
    return flask.Response(
        status="201",
        headers={"Content-Type": "application/json"},
        response=json.dumps(created_event)
    )



@app.patch("/events/<event_id>")
def update_event(event_id):
    pass



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
