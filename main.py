#!/usr/bin/env python3

from flask import Flask, flash, request, redirect, url_for
import json
import random
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

host_ip = '0.0.0.0'
host_port = '7331'
app = Flask(__name__)
auth = HTTPBasicAuth()
app.debug = True
allowed_extensions = {'jpg','mp4','mov','jpeg','png','mkv'}


password = os.environ['password']
upload_folder = os.environ['upload_folder']

users = {
    "theo": generate_password_hash(password)
}

with open('words.json') as f:
    loaded_json = json.load(f)
    animals = loaded_json["animals"]
    adjectives = loaded_json["adjectives"]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/', methods=["GET","POST"])
@auth.login_required
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if allowed_file(uploaded_file.filename):
            random_adj = random.choice(adjectives)
            random_ani = random.choice(animals)
            print("Allowed file")
            filename = uploaded_file.filename
            file_type = filename.rsplit('.', 1)[1]
            file_extension = f".{file_type}"
            print(f"File extension: {file_extension}")
            uploaded_file.save(f"{upload_folder}{random_adj}{random_ani}{file_extension}")
            print(f"File saved as: https://theolikes.tech/files/{random_adj}{random_ani}{file_extension}")
            return(f"https://theolikes.tech/files/{random_adj}{random_ani}{file_extension}")
        return "No file has been uploaded."
    return "Something went wrong."


def main():
    app.run(host=host_ip,port=host_port)

if __name__ == "__main__":
    main()
