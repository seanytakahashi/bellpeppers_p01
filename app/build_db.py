import sqlite

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.executescript("""
DROP TABLE IF EXISTS profiles;
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    country TEXT DEFAULT '',
    balance INTEGER DEFAULT 0
);""")

c.executescript("""
DROP TABLE IF EXISTS blogs;
CREATE TABLE blogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE,
    author TEXT,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    follows INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    FOREIGN KEY (author) REFERENCES profiles(username)
);""")

c.executescript("""
DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    blog INTEGER,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    content TEXT,
    recent_edit DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (blog) REFERENCES blogs(id)
);""")

c.executescript("""
DROP TABLE IF EXISTS edits;
CREATE TABLE edits (
    entry INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_content TEXT,
    FOREIGN KEY (entry) REFERENCES entries(id)
);""")

c.executescript("""
DROP TABLE IF EXISTS follows;
CREATE TABLE follows (
    user TEXT,
    blog INTEGER,
    FOREIGN KEY (user) REFERENCES profiles(username),
    FOREIGN KEY (blog) REFERENCES blogs(id)
);""")


db.commit()
db.close()
