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

# LAB TODOs:
# Implement functions called allowed_file and process_image_file
#
# The allowed_file function should check the file extension
# against the ALLOWED_EXTENSIONS set.
# INPUT: filename - the name of the file to check
# OUTPUT: True if the file has an allowed extension, False otherwise
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# The process_image_file function should:
# INPUT: request - the Flask request object
# OUTPUT: the file path where the image was saved, or None if no valid file was
#         provided
# 1. Check if the 'imageData' key is in the files provided by the request
# 2. If there is no file part, or the file name is empty, return None
# 3. If the file is valid (i.e., exists and has an allowed extension
#   save the file to the IMAGE_FOLDER and return the file path
# 4. This link will help you with saving files in Flask:
#       https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
#   We've done the first set of code, it's your turn to finish it.
#
# You DO NOT need to use the flash messages that the example uses.
def process_image_file(request):
    if 'imageData' not in request.files:
        return None

    file = request.files['imageData']
    if file.filename == "":
        return None

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['IMAGE_FOLDER'], filename)
        file.save(file_path)
        return filename


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
