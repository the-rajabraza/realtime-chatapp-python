from flask import render_template, request, redirect, session
import dbfunctions  # Add this line

def register_routes(app, mysql, session):
    @app.route('/')
    def home():
        return redirect('/login')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            user = dbfunctions.get_user(mysql, username)
            if user is None:
                dbfunctions.add_user(mysql, username)
            session['username'] = username
            session.permanent = True
            return redirect('/users')
        return render_template('login.html')

    @app.route('/users')
    def users():
        if 'username' not in session:
            return redirect('/login')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username FROM users WHERE username != %s', (session['username'],))
        all_users = cursor.fetchall()

        chatted_users = dbfunctions.get_chatted_users(mysql, session['username'])
        chatted_usernames = {user[0] for user in chatted_users}
        available_users = [user for user in all_users if user[0] not in chatted_usernames]

        cursor.close()
        return render_template('users.html', username=session['username'], available_users=available_users, chatted_users=chatted_users)

    @app.route('/chat/<string:partner>')
    def chat(partner):
        if 'username' not in session:
            return redirect('/login')

        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT user1, message, timestamp 
            FROM messages 
            WHERE (user1 = %s AND user2 = %s) OR (user1 = %s AND user2 = %s)
            ORDER BY timestamp ASC
        ''', (session['username'], partner, partner, session['username']))

        messages = cursor.fetchall()
        cursor.close()

        return render_template('chat.html', username=session['username'], partner=partner, messages=messages)
