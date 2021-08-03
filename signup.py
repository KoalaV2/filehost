#!/usr/bin/env python3

import bcrypt
import mariadb
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASSWD = getenv("DB_PASSWD")
DB_IP = getenv("DB_IP")
DB_DATABASE = getenv("DB_DATABASE")


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

salt = bcrypt.gensalt()
c = conn.cursor()


username = input("What is the username? \n :")
password = input("What is the password? \n :")

c.execute("SELECT username from web")
username = username
c.execute(f"SELECT EXISTS(SELECT username FROM web WHERE username='{username}');")
for row in c:
    if row[0] == 1:
        print("Username exists, exiting..")

password = password.encode("utf-8")

hashedpasswd = bcrypt.hashpw(password,salt)
c.execute("INSERT INTO web VALUES (?,?);", (username, hashedpasswd))
conn.commit()


