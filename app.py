import os
from flask import Flask, render_template, g, cli, request, session, redirect, url_for, flash, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import sqlite3
import click
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash 

# Configuration
app = Flask(__name__)
DB = 'app.db'
# -- Very secret key, much hidden, much wow
app.config['SECRET_KEY'] = 'super_duper_massive_hashed_key_shush_no_peeping'
# -- Hot reload so I don't have to restart app all the time
app.config.update(TEMPLATES_AUTO_RELOAD=True)
# -- Login management configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 
login_manager.login_message = "Please log in to access this page." 

# -- User model
class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    # SQL query to get the user by their id
    user_row = db.execute("SELECT id, name, email, password FROM users WHERE id = ?", (user_id,)).fetchone()
    
    if user_row:
        # Create a User object from the row data
        return User(
            id=user_row['id'], 
            name=user_row['name'], 
            email=user_row['email'], 
            password=user_row['password']
        )
    return None

# DB Functions
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DB,
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

app.teardown_appcontext(close_db)


# -- Initialize db and set dummy data
def init_db():
    db = get_db()

    # ---- Hashing dummy passwords
    hashed_admin_pass = generate_password_hash('admin1234')
    hashed_fan_pass = generate_password_hash('test1234')

    # ---- User inserts
    db.executescript(f""" 
        DROP TABLE IF EXISTS users;
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE, 
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
        INSERT INTO users (name, email, password) VALUES ('Admin', 'admin@forum.com', '{hashed_admin_pass}');
        INSERT INTO users (name, email, password) VALUES ('FantasyFan99', 'fan99@forum.com', '{hashed_fan_pass}');
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
        INSERT INTO authors (name, dob) VALUES ('J.K. Rowling', '31-07-1965');
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

# General Routes
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

@app.route("/books")
def books_list():
    db = get_db()
    books = db.execute(
        'SELECT * FROM books ORDER BY authorid'
    ).fetchall()
    return render_template("books.html", books=books)

@app.route("/threads")
def threads_list():
    db = get_db()

    threads = db.execute(
        'SELECT t.id, t.title, t.created_at, b.title AS book_title '
        'FROM threads t '
        'JOIN books b ON t.book_id = b.id '
        'ORDER BY t.created_at DESC'  
    ).fetchall()
    
    return render_template("threads.html", threads=threads)

@app.route("/threads/<int:thread_id>", methods=['GET', 'POST'])
def thread_detail(thread_id):
    db = get_db()

    # ---- Post handling
    if request.method == 'POST':
        # Check if user is logged in
        if not current_user.is_authenticated:
            # We don't use @login_required here because we want to show the thread even if they aren't logged in
            flash("You must be logged in to post a comment.", 'danger')
            return redirect(url_for('login')) # Redirect to login if not authenticated

        content = request.form.get('content')

        # Validate content
        if not content or len(content.strip()) < 5:
            flash("Comment content must be at least 5 characters long.", 'danger')
            # Redirect back to the thread page to see the error flash
            return redirect(url_for('thread_detail', thread_id=thread_id))
        
        try:
            # Insert into posts table
            db.execute(
                "INSERT INTO posts (thread_id, user_id, content, created_at) VALUES (?, ?, ?, DATETIME('now'))",
                (thread_id, current_user.id, content)
            )
            db.commit()
            flash("Your comment was posted successfully!", 'success')
        except sqlite3.Error as e:
            flash(f"A database error occurred while posting: {e}", 'danger')
            print(f"DATABASE ERROR: {e}")

        # Always redirect after a successful POST (or failure) to prevent double submission
        return redirect(url_for('thread_detail', thread_id=thread_id))
    


    # ---- Display the thread
    thread = db.execute(
        'SELECT t.id, t.title, t.created_at, u.name AS thread_starter, '
        'b.title AS book_title, b.description AS book_description '
        'FROM threads t '
        'JOIN users u ON t.user_id = u.id '
        'JOIN books b ON t.book_id = b.id '
        'WHERE t.id = ?',
        (thread_id,)
    ).fetchone()

    if thread is None:
        abort(404)
        
    posts = db.execute(
        'SELECT p.content, p.created_at, u.name AS post_author '
        'FROM posts p '
        'JOIN users u ON p.user_id = u.id '
        'WHERE p.thread_id = ? '
        'ORDER BY p.created_at ASC',
        (thread_id,)
    ).fetchall()

    return render_template('discussion.html', thread=thread, posts=posts)


# AUTH routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        
        # Simple email generation for simplicity's sake
        email = f"{name}@forum.com" 
        
        if not name or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('register'))
        
        db = get_db()
        
        # Check if username (stored in DB 'name' column) already exists
        existing_user = db.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchone()
        if existing_user:
            flash('That username is already taken.', 'danger')
            return redirect(url_for('register'))

        try:
            # Hash the password for secure storage
            password = generate_password_hash(password)

            db.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            db.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            flash(f'A database error occurred: {e}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # --- Debugging Logs Added ---
        print("--- DEBUG: Starting Login Attempt ---")
        
        name = request.form.get('name')
        password = request.form.get('password')
        
        print(f"DEBUG: Form Data Received: Name='{name}', Password is set.") # Never print the password itself
        
        db = get_db()
        # Query the database for the user using the 'name' column
        user_row = db.execute("SELECT id, name, email, password FROM users WHERE name = ?", (name,)).fetchone()
        
        # Check if user exists and password is correct
        if user_row:
            print("DEBUG: User Found in DB.")
            user = User(
                id=user_row['id'], 
                name=user_row['name'], 
                email=user_row['email'], 
                password=user_row['password']
            )
            
            if user.check_password(password):
                print("DEBUG: Password MATCHED! Logging in and redirecting.")
                login_user(user, remember=True) 
                
                
                next_page = request.args.get('next')
                flash(f'Welcome back, {user.name}!', 'success')
                return redirect(next_page or url_for('home'))
            else:
                print("DEBUG: Password FAILED to match.")
        
        else:
            print("DEBUG: User NOT found in database.")

        # If user_row is None OR password check failed, execution falls here
        flash('Invalid username or password.', 'danger')
        print("DEBUG: Login failed. Flashing error and re-rendering login page.")
        print("---------------------------------")


    return render_template('login.html')
@app.route('/logout')
@login_required 
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/create_post')
@login_required
def create_post():
    # TODO: Define post functionality within threads/# 
    return "This is where you can create a post."
    
# Run app
if __name__ == "__main__":
    # Ensure the DB is initialized before starting the app
    with app.app_context():
        init_db() 
    app.run(debug=True)