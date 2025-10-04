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

def init_db():
    db = get_db()

    db.executescript(""" 
        DROP TABLE IF EXISTS 
    """)
# Routes
@app.route("/")
def home():
    return render_template("index.html")

# Run app
if __name__ == "__main__":
    app.run(debug=True)
