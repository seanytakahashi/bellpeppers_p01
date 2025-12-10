# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

import sqlite3
import urllib.request
import urllib.parse
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

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
        case "Dnd":
            path = "https://www.dnd5eapi.co" + path
        case "Species":
            path = "https://ecos.fws.gov/ecp/pullreports/catalog/species/report/species" + path
        case "Countries":
            path = "https://restcountries.com/v3.1" + path
    path += '?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(path) as response:
        data = response.read()
    return json.loads(data)

def findArea(polygon):
    sum1 = 0
    sum2 = 0
    set = polygon.split(",")
    pair1 = []
    pair2 = []
    firstpair = []
    for coords in set:
        pair1 = pair2[:]
        pair2 = coords.split(" ")
        if (len(firstpair) < 1):
            firstpair = coords.split(" ")
        else:
            sum1 += (int(pair1[0])*int(pair2[1]))
            sum2 += (int(pair1[1])*int(pair2[0]))
    sum1 += (int(pair1[0])*int(firstpair[1]))
    sum2 += (int(pair1[1])*int(firstpair[0]))
    return (0.5 * abs(sum1-sum2))

# insert_query("profiles", {"username": "Testing", "password": "Testing"})
# print(general_query("SELECT * FROM profiles WHERE username=?", ["Testing"]))
# print(call_api("Dnd", "/equipment-categories/simple-weapons")["index"])

# print(call_api("Species", "/export", {
#     "format": "json",
#     "columns": "/species@cn,sn,status,range_envelope,gn",
#     "sort": "/species@cn asc;/species@sn asc",
#     "filter": "/species@range_envelope is not null",
#     "filter": "/species@status not in ('Experimental Population, Non-Essential')"
# })["data"][0])