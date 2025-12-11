import sqlite3

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.executescript("""
DROP TABLE IF EXISTS profiles;
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    equipped_weapon TEXT,
    health INTEGER DEFAULT 100,
    country TEXT DEFAULT 'USA',
    balance INTEGER DEFAULT 0
);""")

c.executescript("""
DROP TABLE IF EXISTS fish;
CREATE TABLE fish (
    scientific_name TEXT,
    common_name TEXT,
    owner INTEGER,
    number_caught INTEGER,
    number_owned INTEGER,
    FOREIGN KEY (owner) REFERENCES profiles(id)
);""")

c.executescript("""
DROP TABLE IF EXISTS weapons;
CREATE TABLE weapons (
    name TEXT,
    owner INTEGER,
    durability INTEGER,
    FOREIGN KEY (owner) REFERENCES profiles(id)
);""")

db.commit()
db.close()
