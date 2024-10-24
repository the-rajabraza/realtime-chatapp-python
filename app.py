from flask import Flask, session, redirect, request, url_for
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
import dbconfig
import dbfunctions
import os
from routes import register_routes
from socketio_handling import register_socketio_handlers
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set session timeout to 30 minutes

socketio = SocketIO(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = dbconfig.MYSQL_HOST
app.config['MYSQL_USER'] = dbconfig.MYSQL_USER
app.config['MYSQL_PASSWORD'] = dbconfig.MYSQL_PASSWORD
app.config['MYSQL_DB'] = dbconfig.MYSQL_DB

mysql = MySQL(app)

# Initialize the database
with app.app_context():
    dbfunctions.init_db(mysql)

# Authentication check
@app.before_request
def check_auth():
    if request.endpoint and 'static' not in request.endpoint and request.endpoint != 'login':
        if 'username' not in session:
            return redirect(url_for('login'))

# Register routes and socketio handlers
register_routes(app, mysql, session)
register_socketio_handlers(socketio, mysql)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
