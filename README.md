```markdown
# Real-Time Chat Web Application

A real-time chat web application built with Flask, Flask-SocketIO, and Flask-MySQLdb. This project allows users to join rooms and communicate with each other in real-time.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Application](#running-the-application)

## Features

- Real-time messaging using WebSockets
- User sessions with Flask session management
- Room-based chat functionality
- MySQL database integration

## Technologies Used

- [Flask](https://flask.palletsprojects.com/) - A micro web framework for Python.
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/) - Enables WebSocket communication.
- [Flask-MySQLdb](https://flask-mysqldb.readthedocs.io/) - MySQL database integration with Flask.
- [Python](https://www.python.org/) - The programming language used for the backend.

## Installation

### Prerequisites

- Python
- MySQL Server


### Create a Virtual Environment (Optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install Flask Flask-SocketIO Flask-MySQLdb
```

### Create `requirements.txt`

```bash
pip freeze > requirements.txt
```

## Usage

1. Configure your database connection in `dbconfig.py`.
2. Implement your database functions in `dbfunctions.py`.
3. Start the Flask application.

## Running the Application

```bash
python app.py
```

By default, the application will run on `http://127.0.0.1:5000/`.