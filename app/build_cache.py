import sqlite3

DB_FILE = "cache.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.executescript("""
DROP TABLE IF EXISTS fish;
CREATE TABLE fish (
    scientific_name TEXT UNIQUE PRIMARY KEY,
    scientific_name TEXT,
    status TEXT,
    range INTEGER,
    type TEXT
);""")

c.executescript("""
DROP TABLE IF EXISTS weapons;
CREATE TABLE weapons (
    name TEXT UNIQUE PRIMARY KEY,
    damage_dice STRING,
    damage_type TEXT,
    max_durability INTEGER,
    range INTEGER
);""")

db.commit()
db.close()
