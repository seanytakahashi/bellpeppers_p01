# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

import utility
import battle
import random
import time
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

bp = Blueprint('fish', __name__, url_prefix='/fish')

def get_fish():
    fishSet = utility.call_api("Species", "/export", [
        ("format", "json"),
        ("distinct", "true"),
        ("columns", "/species@cn,sn,status,range_envelope,gn"),
        ("sort", "/species@cn asc;/species@sn asc"),
        ("filter", "/species@cn not like '%no common name%'"),
        ("filter", "/species@cn not like '%unnamed%'"),
        ("filter", "/species@range_envelope is not null"),
        ("filter", "/species@gn != 'Algae'"),
        ("filter", "/species@gn != 'Conifers and Cycads'"),
        ("filter", "/species@gn != 'Ferns and Allies'"),
        ("filter", "/species@gn != 'Flowering Plants'"),
        ("filter", "/species@gn != 'Lichens'"),
        ("filter", "/species@status in ('Resolved Taxon','Species of Concern','Threatened','Endangered','Extinction')")
    ])["data"]
    # x = 0
    for fish in fishSet:
        # x += 1
        try:
            fish[3] = utility.find_area(fish[3][9:-2])
        except:
            print(fish[0])
            print(fish[3])
    raw = random.choice(fishSet)
    fish = {
        "scientific_name": raw[1]["value"],
        "common_name": raw[0],
        "status": raw[2],
        "range": raw[3],
        "type": raw[4]
    }
    utility.cache_entry("fish", fish)
    return fish

# @bp.get("/")
# def fish():
#     chance = random.randint(1, 100)
#     if (randint > 90): # treasure chance: ~10%
#         print("treasure caught. debug console message for now")
#         return "you found treasure"
#     else # call the database, then send the result to battle
#         fish = get_fish


# TESTING
@bp.get("catch_weapon")
def catch_weapon_get():
    weapon = battle.get_random_weapon()
    user = utility.get_user(session["username"])
    # Should only go into inventory; Goes directly to equipped for testing
    utility.general_query("UPDATE profiles SET equipped_weapon=? WHERE username=?", [weapon['name'], session["username"]])
    utility.insert_query("weapons", {"name": weapon['name'], "owner": user['id'], "durability": weapon['max_durability']})
    return redirect(url_for('profile_get'))

# print(get_fish())
