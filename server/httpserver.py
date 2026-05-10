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


@app.post("/requests")
def submit_request():
    data = request.get_json()
    request_name = data.get("name")
    dataservice.add_request(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
