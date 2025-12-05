# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

import sqlite3

DB_FILE = "data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)

def insert_query(table, data):
    c = db.cursor()
    placeholder = ["?"] * len(data)
    c.execute(f"INSERT INTO {table} {tuple(data.keys())} VALUES ({', '.join(placeholder)}) RETURNING *;", tuple(data.values()))
    c.close()
    db.commit()
