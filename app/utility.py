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

CACHE_FILE = "cache.db"
cache = sqlite3.connect(CACHE_FILE, check_same_thread=False)

species_list = ['Insects', 'Arachnids', 'Snails', 'Clams', 'Birds', 'Mammals', 'Fishes', 'Crustaceans', 'Reptiles', 'Amphibians', 'Flatworms and Roundworms', 'Sponges', 'Annelid Worms']
species_dict = {"Insects":15.0, "Fishes":2000.0}

def dictify(raw, c):
    output = []
    for row in raw:
        d = dict()
        for col in range(len(row)):
            d.update({c.description[col][0]: row[col]})
        output.append(d)
    return output

# data: {"keys", value}
# FIRST KEY VALUE PAIR MUST BE PRIMARY KEY
def cache_entry(table, data):
    c = cache.cursor()
    c.execute(f"SELECT * FROM {table} WHERE {list(data)[0]}=?", [list(data.values())[0]])
    if c.fetchone() is None:
        placeholder = ["?"] * len(data)
        c.execute(f"INSERT INTO {table} {tuple(data.keys())} VALUES ({', '.join(placeholder)});", tuple(data.values()))
    c.close()
    cache.commit()

# query: ("key", value)
def pull_cache(table, query):
    c = cache.cursor()
    c.execute(f"SELECT * FROM {table} WHERE {query[0]}=?", [query[1]])
    output = dictify(c.fetchall(), c)[0] or None
    c.close()
    return output

# data: "key": value}
def insert_query(table, data):
    c = db.cursor()
    placeholder = ["?"] * len(data)
    c.execute(f"INSERT INTO {table} {tuple(data.keys())} VALUES ({', '.join(placeholder)});", tuple(data.values()))
    c.close()
    db.commit()

# params: [val1, val2]
# returns [{'key1': val1}]
def general_query(query_string, params=()):
    c = db.cursor()
    c.execute(query_string, params)
    raw = c.fetchall()
    output = dictify(raw, c)
    c.close()
    db.commit()
    return output

def get_user(name):
    user = general_query(f"SELECT * FROM profiles WHERE username=?", [name])
    return None if len(user) == 0 else user[0]

# params: [("key", value)]
def call_api(api_name, path, params=[]):
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

def find_area(polygon):
    sum2 = 0
    sum1 = 0
    polygon.replace(" ", ",")
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
            sum1 += (float(pair1[0])*float(pair2[1]))
            sum2 += (float(pair1[1])*float(pair2[0]))
    sum1 += (float(pair1[0])*float(firstpair[1]))
    sum2 += (float(pair1[1])*float(firstpair[0]))
    return (int)(0.5 * abs(sum1-sum2))

# insert_query("profiles", {"username": "Testing", "password": "Testing"})
# print(general_query("SELECT * FROM profiles WHERE username=?", ["test"]))
# print(call_api("Dnd", "/equipment-categories/simple-weapons")["index"])

# print(call_api("Species", "/export", {
#     "format": "json",
#     "columns": "/species@cn,sn,status,range_envelope,gn",
#     "sort": "/species@cn asc;/species@sn asc",
#     "filter": "/species@range_envelope is not null",
#     "filter": "/species@status not in ('Experimental Population, Non-Essential')"
# })["data"][0])
