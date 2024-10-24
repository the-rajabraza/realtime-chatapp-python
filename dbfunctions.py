# dbfunctions.py

from flask_mysqldb import MySQL

def init_db(mysql):
    with mysql.connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user1 VARCHAR(100),
                user2 VARCHAR(100),
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                username VARCHAR(100) NOT NULL,
                avatar VARCHAR(255) DEFAULT NULL,
                status_message VARCHAR(255) DEFAULT NULL,
                PRIMARY KEY (username),
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS read_receipts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message_id INT NOT NULL,
                reader VARCHAR(100) NOT NULL,
                read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
                FOREIGN KEY (reader) REFERENCES users(username) ON DELETE CASCADE
            )
        ''')
        mysql.connection.commit()

def add_user(mysql, username):
    with mysql.connection.cursor() as cursor:
        cursor.execute('INSERT INTO users (username) VALUES (%s)', (username,))
        cursor.execute('INSERT INTO user_profiles (username) VALUES (%s)', (username,))
        mysql.connection.commit()

def get_user(mysql, username):
    with mysql.connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        return cursor.fetchone()

def get_chatted_users(mysql, username):
    with mysql.connection.cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT 
                CASE 
                    WHEN user1 = %s THEN user2 
                    ELSE user1 
                END AS chat_user
            FROM messages
            WHERE user1 = %s OR user2 = %s
        ''', (username, username, username))
        return cursor.fetchall()

def save_message(mysql, user1, user2, message):
    with mysql.connection.cursor() as cursor:
        cursor.execute('INSERT INTO messages (user1, user2, message) VALUES (%s, %s, %s)',
                       (user1, user2, message))
        mysql.connection.commit()
        return cursor.lastrowid

def get_user_profile(mysql, username):
    with mysql.connection.cursor() as cursor:
        cursor.execute('SELECT * FROM user_profiles WHERE username = %s', (username,))
        return cursor.fetchone()

def update_user_profile(mysql, username, avatar, status_message):
    with mysql.connection.cursor() as cursor:
        cursor.execute('UPDATE user_profiles SET avatar = %s, status_message = %s WHERE username = %s',
                       (avatar, status_message, username))
        mysql.connection.commit()

def mark_message_as_read(mysql, message_id, reader):
    with mysql.connection.cursor() as cursor:
        cursor.execute('INSERT INTO read_receipts (message_id, reader) VALUES (%s, %s)',
                       (message_id, reader))
        mysql.connection.commit()

def get_unread_messages(mysql, username, partner):
    with mysql.connection.cursor() as cursor:
        cursor.execute('''
            SELECT m.id, m.message, m.timestamp
            FROM messages m
            LEFT JOIN read_receipts r ON m.id = r.message_id AND r.reader = %s
            WHERE ((m.user1 = %s AND m.user2 = %s) OR (m.user1 = %s AND m.user2 = %s))
            AND r.id IS NULL
            ORDER BY m.timestamp ASC
        ''', (username, partner, username, username, partner))
        return cursor.fetchall()