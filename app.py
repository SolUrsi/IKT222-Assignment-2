# Imports
from flask import Flask, render_template, g, cli
import sqlite3
import click
from datetime import datetime

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

    # ---- User inserts
    db.executescript(""" 
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
        INSERT INTO users (name, email, password) VALUES ('Admin', 'admin@forum.com', 'admin1234');
        INSERT INTO users (name, email, password) VALUES ('FantasyFan99', 'fan99@forum.com', 'test1234');
    """)
    db.commit()

    # ---- Author inserts
    db.executescript(""" 
        DROP TABLE IF EXISTS authors;
        CREATE TABLE authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dob TEXT NOT NULL
        );
        INSERT INTO authors (name, dob) VALUES ('Rick Riordan', '05-06-1964');
        INSERT INTO authors (name, dob) VALUES ('Christopher Paolini', '17-11-1983');
        INSERT INTO authors (name, dob) VALUES ('Rick Riordan', '31-07-1965');
    """)
    db.commit()

    # ---- Book inserts
    db.executescript(""" 
        DROP TABLE IF EXISTS books;
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            genre TEXT NOT NULL,
            authorid INTEGER,
            FOREIGN KEY (authorid) REFERENCES authors(id)
        );
        -- Rick Riordan, Percy Jackson
        INSERT INTO books (title, description, genre, authorid) VALUES (
        'The Lightning Thief',
        'Twelve-year-old Percy Jackson discovers he is a demigod, the son of Poseidon, and must go on a quest to retrieve Zeus''s stolen lightning bolt to prevent a war among the Olympian gods.',
        'Fantasy/Greek Mythology',
        1

        );
        INSERT INTO books (title, description, genre, authorid) VALUES (
        'The Sea of Monsters',
        'Percy and his friends must journey into the Sea of Monsters (the Bermuda Triangle) to find the mythical Golden Fleece, which is the only thing that can save Camp Half-Blood from destruction.',
        'Fantasy/Greek Mythology',
        1
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'The Titan''s Curse',
        'Percy joins a mission to rescue the goddess Artemis and his friend Annabeth after they are captured. They must face a powerful new Titan threat and a deadly curse.',
        'Fantasy/Greek Mythology',
        1
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'The Battle of the Labyrinth',
        'To stop the Titan Lord Kronos from invading Camp Half-Blood, Percy and his companions must navigate the deadly, magical Labyrinth, a maze with entrances across the world.',
        'Fantasy/Greek Mythology',
        1
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'The Last Olympian',
        'As Kronos gathers his forces, Percy and the remaining Olympian gods and demigods prepare for the final showdown to defend Mount Olympus in New York City.',
        'Fantasy/Greek Mythology',
        1
        );

        -- Christopher Paolini, Inheritance Cycle
        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Eragon',
        'A young farm boy, Eragon, discovers a mysterious stone that hatches into a dragon, Saphira. He is thrust into a destiny as a Dragon Rider and joins the rebellion against the evil King Galbatorix.',
        'High Fantasy',
        2
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Eldest',
        'Eragon travels to the Elven capital, Ellesméra, to continue his training in sword fighting and magic under the guidance of the crippled Dragon Rider, Oromis, while war looms over the land of Alagaësia.',
        'High Fantasy',
        2
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Brisingr',
        'As the war intensifies, Eragon must make a choice between his loyalty to the Varden and the need to protect his cousin Roran, all while dealing with powerful new magical abilities and a dangerous prophecy.',
        'High Fantasy',
        2
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Inheritance',
        'The final confrontation. Eragon and Saphira lead the free people of Alagaësia in the ultimate battle against the tyrant King Galbatorix to determine the future of the Dragon Riders and the entire realm.',
        'High Fantasy',
        2
        );

        -- J.K. Rowling, Harry Potter
        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Harry Potter and the Philosopher''s Stone',
        'An orphaned boy, Harry Potter, discovers on his eleventh birthday that he is a wizard and is invited to study at the magical Hogwarts School of Witchcraft and Wizardry.',
        'Fantasy',
        3
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Harry Potter and the Chamber of Secrets',
        'Harry returns for his second year and must face a mysterious force that is petrifying students at Hogwarts, uncovering a deadly secret hidden within the school.',
        'Fantasy',
        3
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Harry Potter and the Prisoner of Azkaban',
        'A dangerous wizard and escaped prisoner, Sirius Black, is hunting Harry. Harry learns about his parents'' past and discovers a secret about Black''s true identity.',
        'Fantasy',
        3
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Harry Potter and the Goblet of Fire',
        'Harry is mysteriously selected as a champion in the dangerous Triwizard Tournament, leading to the shocking and public return of Lord Voldemort.',
        'Fantasy',
        3
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Harry Potter and the Order of the Phoenix',
        'As the wizarding world denies Voldemort''s return, Harry struggles with his isolation and prophecy while fighting to prove the dark lord is back, forming a secret defense group.',
        'Fantasy',
        3
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Harry Potter and the Half-Blood Prince',
        'Harry discovers a mysterious old textbook that aids him in class, while he and Dumbledore delve into Voldemort''s past to find the secret to his immortality.',
        'Fantasy',
        3
        );

        INSERT INTO books (title, description, genre, authorid) VALUES (
        'Harry Potter and the Deathly Hallows',
        'In the final installment, Harry, Ron, and Hermione abandon Hogwarts to hunt down and destroy the remaining Horcruxes, leading to the climactic final battle.',
        'Fantasy',
        3
        );
    """)
    db.commit()

    # ---- Thread
    db.executescript(""" 
        DROP TABLE IF EXISTS threads;
        CREATE TABLE threads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        -- Sample Threads:

        -- Discussion about HP and the Deathly Hallows (ID 5), started by Admin (ID 1)
        INSERT INTO threads (book_id, user_id, title, created_at) VALUES (
            5, 
            1, 
            'The Epilogue: Did it work or not?', 
            DATETIME('now', '-2 day')
        ); 
        -- Review of The Lightning Thief (ID 1) by FantasyFan99 (ID 2)
        INSERT INTO threads (book_id, user_id, title, created_at) VALUES (
            1, 
            2, 
            'My first impressions of Camp Half-Blood!', 
            DATETIME('now', '-1 day')
        );
    """)
    db.commit()

    # ---- Posts
    db.executescript(""" 
        DROP TABLE IF EXISTS posts;
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (thread_id) REFERENCES threads(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        -- Sample Posts
        INSERT INTO posts (thread_id, user_id, content, created_at) VALUES (
            1, 
            1, 
            'I felt the HP epilogue was a little too neat and tidy. What are your thoughts on the happily-ever-after ending?', 
            DATETIME('now', '-2 day')
        );
        INSERT INTO posts (thread_id, user_id, content, created_at) VALUES (
            1, 
            2, 
            'I loved it! It gave the characters the closure they deserved after all the fighting.', 
            DATETIME('now', '-1 day')
        );
        INSERT INTO posts (thread_id, user_id, content, created_at) VALUES (
            2, 
            2, 
            'Percy is such a fun narrator. The quest to the underworld felt incredibly epic for a first book!', 
            DATETIME('now', '-10 hours')
        );
    """)

    print("Database initialized")


# Flask CLI initialize DB
@app.cli.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

# Routes
# -- Use Jinja to format HTML ( {% %} )
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/authors")
def authors_list():
    db = get_db()
    authors = db.execute(
        'SELECT * FROM authors ORDER BY name'
    ).fetchall()

    return render_template("authors.html", authors=authors)
# Run app
if __name__ == "__main__":
    app.run(debug=True)
