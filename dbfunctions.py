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
        mysql.connection.commit()

def add_user(mysql, username):
    with mysql.connection.cursor() as cursor:
        cursor.execute('INSERT INTO users (username) VALUES (%s)', (username,))
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
