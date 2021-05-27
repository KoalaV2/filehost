#!/usr/bin/env python3

from flask import Flask, flash, request, redirect, url_for
from random_word import RandomWords

HOST_IP = '0.0.0.0'
HOST_PORT = '7331'
app = Flask(__name__)
app.debug = True
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'jpg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        uploaded_file.save(f"{UPLOAD_FOLDER}/file.jpg")
        return "File has been uploaded"
    return "No file has been uploaded"


def main():
    app.run(host=HOST_IP,port=HOST_PORT)

if __name__ == "__main__":
    main()
