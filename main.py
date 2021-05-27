#!/usr/bin/env python3

from flask import Flask, flash, request, redirect, url_for
import json

host_ip = '0.0.0.0'
host_port = '7331'
app = Flask(__name__)
app.debug = True
upload_folder = 'uploads/'
allowed_extensions = {'jpg','mp4','mov','jpeg','png'}

with open('words.json') as f:
    loaded_json = json.load(f)
    animals = loaded_json["animals"]
    adjectives = loaded_json["adjectives"]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/', methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if allowed_file(uploaded_file.filename):
            print("Allowed file")
            filename = uploaded_file.filename
            file_type = filename.rsplit('.', 1)[1]
            file_extension = f".{file_type}"
            print(f"File extension: {file_extension}")
            uploaded_file.save(f"{upload_folder}lmao{file_extension}")
            return(f"File saved as: https://f.theolikes.tech/{upload_folder}lmao{file_extension}")
        return "No file has been uploaded."
    return "Something went wrong."


def main():
    app.run(host=host_ip,port=host_port)

if __name__ == "__main__":
    main()
