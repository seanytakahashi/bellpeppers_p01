# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

import sqlite3
import utility
import fish

DB_FILE = "cache.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.executescript("""
DROP TABLE IF EXISTS fish;
CREATE TABLE fish (
    scientific_name TEXT UNIQUE PRIMARY KEY,
    common_name TEXT,
    status TEXT,
    accuracy INTEGER,
    type TEXT
);""")

c.executescript("""
DROP TABLE IF EXISTS weapons;
CREATE TABLE weapons (
    name TEXT UNIQUE PRIMARY KEY,
    damage_dice STRING,
    max_durability INTEGER,
    accuracy INTEGER
);""")

db.commit()
db.close()

# Initialize Cache
try:
    all_weapons = utility.call_api("Dnd", "/api/2014/equipment-categories/simple-weapons")["equipment"]
    for i in range(6):
        raw = utility.call_api("Dnd", all_weapons[i]["url"])
        weapon = {
            "name": raw["name"],
            "damage_dice": raw["damage"]["damage_dice"],
            "max_durability": max(raw["weight"], 1) * 10,
            "accuracy": min(100, raw["range"]["normal"] * 10)
        }
        utility.cache_entry("weapons", weapon)

    fish.get_fish()
except:
    print("Building Cache Failed; APIs are unresponsive")