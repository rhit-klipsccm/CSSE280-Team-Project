import flask
import json
import dataservice
import os
from flask import request

from werkzeug.utils import secure_filename

app = flask.Flask(__name__,
            static_url_path='',
            static_folder='dist')


@app.get("/shutdown")
def shutdown():
    os._exit(0)

@app.get("/requests")
def get_requests():
    requests = dataservice.get_all_requests()
    return flask.Response(
        status="200 OK",
        headers={"Content-Type": "application/json"},
        response=josn.dumps(requests)
    )

@app.post("/requests")
def submit_request():
    data = request.get_json()
    dataservice.add_request(data)
    return flask.redirect("/index.html")

@app.patch("/requests/<request_id>")
def update_request(request_id):
    data = request.get_json()
    
    ## TODO: Implement the following fields on the admin page:
    approval_action = data.get("action")
    reason = data.get("reason")

    dataservice.patch_request(request_id, approval_action, reason)
    return flask.redirect("/admin.html")

@app.delete("/requests/<request_id>")
def delete_request(request_id):
    if dataservice.verify_entry_exists(request_id):
        dataservice.delete_request(request_id)
    return flask.redirect("/admin.html")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
