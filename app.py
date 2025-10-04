# Imports
from flask import Flask, render_template, g
import sqlite3

# Configuration
DB = 'app.db'

# Initialization
app = Flask(__name__)

# DB Functions
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DB,
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()

app.teardown_appcontext(close_db)

# -- Initialize db and set dummy data
def init_db():
    db = get_db()

    db.executescript(""" 
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
        INSERT INTO users (name, email, password) VALUES ('Test User', 'test@uia.no', '1234');
    """)
    db.commit()
    db.executescript(""" 
        DROP TABLE IF EXISTS books;
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            password TEXT NOT NULL
        );
        INSERT INTO users (name, email, password) VALUES ('Test User', 'test@uia.no', '1234');
    """)
    print("Database initialized")

# Routes
@app.route("/")
def home():
    return render_template("index.html")

# Run app
if __name__ == "__main__":
    app.run(debug=True)
