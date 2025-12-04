<<<<<<< HEAD
import sqlite3

DB_FILE = "data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)

def insert_query(table, data):
    c = db.cursor()
    placeholder = ["?"] * len(data)
    c.execute(f"INSERT INTO {table} {tuple(data.keys())} VALUES ({', '.join(placeholder)}) RETURNING *;", tuple(data.values()))
    c.close()
    db.commit()
=======
# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m
>>>>>>> 405998bb2567675e39ae4ce722df3d2b27b9c6c2
