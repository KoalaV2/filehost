#!/usr/bin/env python3

from flask import Flask, flash, request, redirect, url_for, render_template
import json
import random
import mariadb
from os import getenv
from dotenv import load_dotenv
import bcrypt

host_ip = '0.0.0.0'
host_port = '7331'

app = Flask(__name__)
app.debug = True
allowed_extensions = {'jpg','mp4','mov','jpeg','png','mkv'}

load_dotenv()
DB_USER = getenv("DB_USEr")
DB_PASSWD = getenv("DB_PASSWD")
DB_IP = getenv("DB_IP")
DB_DATABASE = getenv("DB_DATABASE")
UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")


try:
    conn = mariadb.connect(
        user=DB_USER,
        password=DB_PASSWD,
        host=DB_IP,
        port=3306,
        database=DB_DATABASE

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    exit()

with open('words.json') as f:
    loaded_json = json.load(f)
    animals = loaded_json["animals"]
    adjectives = loaded_json["adjectives"]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


class User:
    def __init__(self):
        self.salt = bcrypt.gensalt()
        self.c = conn.cursor()
    def login(self,username,password):
        print("Querying..")
        self.c.execute(f"SELECT username,password from web WHERE username='{username}'")
        for row in self.c:
            hashedpasswd = row[1].encode("utf-8")
            print(f"Hashed password from database: {hashedpasswd}")
            password = password.encode("utf-8")
            if bcrypt.checkpw(password,hashedpasswd):
                print(f"Welcome {username} you have been logged in.")
                return(f"Welcome {username} you have been logged in.")
            else:
                print("Wrong username or password")
                return("Wrong username or password.")
        print("No user with that username found.")
        self.c.close()
        return("No user with that username found.")

@app.route('/', methods=["GET","POST"])
def upload_file():
    user = User()
    if request.method == 'POST':
        username = request.authorization.username
        password = request.authorization.password
        if user.login(username,password):
            uploaded_file = request.files['file']
            if allowed_file(uploaded_file.filename):
                randomAdjective = random.choice(adjectives)
                randomAnimal = random.choice(animals)
                print("Allowed file")
                filename = uploaded_file.filename
                fileType = filename.rsplit('.', 1)[1]
                fileExtension = f".{fileType}"
                print(f"File extension: {fileExtension}")
                uploaded_file.save(f"{UPLOAD_FOLDER}{randomAdjective}{randomAnimal}{fileExtension}")
                print(f"File saved as: https://theolikes.tech/files/{randomAdjective}{randomAnimal}{fileExtension}")
                return(f"https://theolikes.tech/files/{randomAdjective}{randomAnimal}{fileExtension}")
            return "No file has been uploaded. File extension now allowed."
    if request.method == 'GET':
        return render_template("index.html")


def main():
    app.run(host=host_ip,port=host_port)

if __name__ == "__main__":
    main()
