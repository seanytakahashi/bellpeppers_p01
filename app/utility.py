# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

import sqlite3
import urllib.request
import urllib.parse
import json

DB_FILE = "data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)

# data: {"key": value}
def insert_query(table, data):
    c = db.cursor()
    placeholder = ["?"] * len(data)
    c.execute(f"INSERT INTO {table} {tuple(data.keys())} VALUES ({', '.join(placeholder)});", tuple(data.values()))
    c.close()
    db.commit()

# params: [val1, val2]
def general_query(query_string, params=()):
    c = db.cursor()
    c.execute(query_string, params)
    output = c.fetchall()
    c.close()
    db.commit()
    return output

# params: {"key": value}
def call_api(api_name, path, params={}):
    match api_name:
        case "DND":
            path = "https://www.dnd5eapi.co/api/2014/" + path
        case "Species":
            path = "https://ecos.fws.gov/ecp/pullreports/catalog/species/report/species/export" + path
        case "Countries":
            path = "https://restcountries.com/v3.1/" + path
    path += urllib.parse.urlencode(params)
    with urllib.request.urlopen(path) as response:
        data = response.read()
    return json.loads(data);

# insert_query("profiles", {"username": "Testing", "password": "Testing"})
# print(general_query("SELECT * FROM profiles WHERE username=?", ["Testing"]))
# print(call_api("DND", "equipment-categories/simple-weapons")["index"])
