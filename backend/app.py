from flask import Flask
from flask import session
from flask import request
from flask import redirect, url_for
from flask import g
from flask_socketio import SocketIO
from schema import Schema, And, Use, Optional, SchemaError
import json
import sqlite3
import bcrypt

# App config
app = Flask(__name__)
app.secret_key = open(".secret_key").read()
# socketio = SocketIO(app)


# Opening the local db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("persistence.db")
    return db

# Closing db connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Opening the local db
conn = sqlite3.connect('persistence.db')  # Creates a new database file if it doesn’t exist
# Making sure all the schemes are existent
conn.executescript("""
    BEGIN;
    CREATE TABLE IF NOT EXISTS users(username, password);
    CREATE TABLE IF NOT EXISTS departures(destination, departure, flight, airline, terminal, status);
    CREATE TABLE IF NOT EXISTS arrivals(origin, arrival, flight, airline, terminal, status);
    COMMIT;
""")
conn.close()

# Check for hashed password and sanitized sql query
def check_password(username, password):
    user_password = get_db().execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
    if user_password == None:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), user_password[0].encode('utf-8'))


# Login endpoint for airport employees so they can publish new events and info
@app.route("/api/login", methods=['POST'])
def admin_login():
    if check_password(request.form['username'], request.form['password']):
        session['admin_session'] = request.form['username']
        return {
            "status": "OK"
        }
    else:
        return {
            "status": "Access denied"
        }



# todo: list all info about departures and arrivals
# todo: endpoint so only authenticated employees can publish new info and being saved in the db



# @app.route("/api/flights", methods=['GET'])
# def get_flights():
#     return {}

# @app.route("/api/flights", methods=['POST'])
# def add_flights():
#     if 'admin_session' not in session:
#         return {
#             "error": "Unauthorized access"
#         }

#     if not check(conf_schema, request.get_json()):
#         return {
#             "status": "error parsing json"
#         }

#     return request.get_json()


# def check(conf_schema, conf):
#     try:
#         conf_schema.validate(conf)
#         return True
#     except SchemaError:
#         return False

# conf_schema = Schema({
#     'destination': And(Use(str)),
#     'departure': And(Use(str)),
#     'flight': And(Use(str)),
#     'airline': And(Use(str)),
#     'terminal': And(Use(int)),
#     'status': And(Use(str)),
# })






# Auth routes
# @app.route('/')
# def index():
#     if 'username' in session:
#         return f'Logged in as {session["username"]}'
#     elif 'unique_id' in session:
#         return f'Logged with unique_id of {session["unique_id"]}'
#     return 'You are not logged in'

# @app.route("/api/login/user", methods=['POST'])
# def user_login():
#     session['unique_id'] = request.form['unique_id']
#     return {
#         "status": "OK"
#     }
#

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))


# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('message')
# def handle_message(data):
#     print('Received message:', data)
#     socketio.emit('response', 'Server received your message: ' + data)

