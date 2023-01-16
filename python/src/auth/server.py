import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environment.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environment.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environment.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environment.get("MYSQL_DB")
server.config["MYSQL_PORT "] = os.environment.get("MYSQL_PORT")

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing Credentials", 401
        