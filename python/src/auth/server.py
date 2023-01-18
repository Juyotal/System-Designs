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
    
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0: 
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid Credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else: 
        return "Invalid Credentials", 401


@server.route("/validate", method=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200

def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.datetime.utcnow(),
            "admin": authz
        },
        secret,
        algorithm = "HS256"
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
