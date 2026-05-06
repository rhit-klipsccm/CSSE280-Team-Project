import flask
import json
import dataservice
import os
from flask import request

# This portion is for the lab, we'll talk about it before you start that

from werkzeug.utils import secure_filename
IMAGE_FOLDER = 'public/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# End lab portion

app = flask.Flask(__name__,
            static_url_path='',
            static_folder='public')

# One more line for the lab
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER



@app.get("/shutdown")
def shutdown():
    os._exit(0)


@app.get("/list")
def get_list():
    print(json.dumps(dataservice.get_shopping_list()))
    return flask.Response(status="200 OK",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_shopping_list()))

@app.post("/list/<item>")
def post_list_item(item):
    dataservice.add_item_to_list(item)
    return flask.Response(status="201 Created",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_shopping_list()))


@app.post("/list/image")
def add_image_to_item():
    
    # LAB TODO: Implement this function to use the methods specified below.
    # If a file is included and valid, save it and add the item with image path.
    # If no file is included, just add the item without an image.
    # To access form data in Flask, use flask.request.form['fieldName']
    #
    # When done, follow the instructions in zyBook to submit.
    # Redirect the user (using the flask redirect built-in) to /shopping.html.
    item_name = request.form['itemWithImageName']
    filename = process_image_file(request)
    if filename is None:
        dataservice.add_item_to_list(item_name)
    else:
        filepath = "images/" + filename
        dataservice.add_item_with_image(item_name, filepath)
    return flask.redirect("http://localhost:8080/shopping.html")




@app.patch("/list/<item>")
def patch_list_item(item):
    #request_body = flask.request.get_json()
    dataservice.move_item_between_lists(item)
    return flask.Response(status="200 OK",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_shopping_list()))


@app.delete("/list/<item>")
def delete_list_item(item):
    dataservice.remove_item(item)
    return flask.Response(status="200 OK",
                          headers={"Content-Type": "application/json"},
                          response = json.dumps(dataservice.get_shopping_list()))

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
