from flask import Flask
from flask import session
from flask import request
from flask import redirect, url_for
from flask_socketio import SocketIO
import json


# todo: TEMPORAL DO NOT LEAVE LIKE THIS
# Load credentials into hashmap for quick access
json_file = open('credentials_temp.json')
data = json.load(json_file)
credentials = dict()
for c in data:
    credentials.update(c)

print(credentials)


app = Flask(__name__)
# todo: Temporal put in .env or something
app.secret_key = b'd0ce0c45db61bb87d0f0ddd821314cd6c90440dd580a7f15a005a2ed84010d11'
socketio = SocketIO(app)


@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    elif 'unique_id' in session:
        return f'Logged with unique_id of {session["unique_id"]}'
    return 'You are not logged in'

@app.route("/api/login/user", methods=['POST'])
def user_login():
    session['unique_id'] = request.form['unique_id']
    return {
        "status": "OK"
    }

@app.route("/api/login/admin", methods=['POST'])
def admin_login():
    if credentials[request.form['username']] == request.form['password']:
        session['username'] = request.form['username']
        return {
            "status": "OK"
        }
    else:
        return {
            "status": "Access denied"
        }

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
