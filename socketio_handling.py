from flask_socketio import join_room, emit
from flask import session  # Import session
import dbfunctions

def register_socketio_handlers(socketio, mysql):
    @socketio.on('connect')
    def handle_connect():
        username = session.get('username')  # Now this should work
        if username:
            join_room(username)

    @socketio.on('send_message')
    def handle_message(data):
        message = data['message']
        username = data['username']
        partner = data['partner']

        # Save the message to the database
        dbfunctions.save_message(mysql, username, partner, message)

        # Emit the message to both users
        emit('receive_message', {'message': message, 'username': username}, room=partner)
        emit('receive_message', {'message': message, 'username': username}, room=username)
