from flask import Flask, session, redirect
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
import dbconfig
import dbfunctions
import os
from routes import register_routes
from socketio_handling import register_socketio_handlers

app = Flask(__name__)
app.secret_key = os.urandom(24)
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

# Register routes and socketio handlers
register_routes(app, mysql, session)
register_socketio_handlers(socketio, mysql)

if __name__ == '__main__':
    socketio.run(app, host='192.168.0.248', port=5000, debug=True)
