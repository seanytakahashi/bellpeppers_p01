# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

import utility
import battle
import random
import travel
from flask import Blueprint, redirect, url_for, session, flash

bp = Blueprint('fish', __name__, url_prefix='/fish')

def get_fish(filter="%"):
    try:
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
            ("filter", "/species@status in ('Resolved Taxon','Species of Concern','Threatened','Endangered','Extinction')"),
            ("filter", f"/species@gn like '{filter}'")
        ])["data"]

        for fish in fishSet:
            fish[3] = utility.find_area(fish[3][9:-2])
        
        raw = random.choice(fishSet)
        fish = {
            "scientific_name": raw[1]["value"],
            "common_name": raw[0],
            "status": raw[2],
            "accuracy": min(100, raw[3]),
            "type": raw[4]
        }

        utility.cache_entry("fish", fish)
    except Exception:
        fish = utility.query_cache("SELECT * FROM fish ORDER BY random() LIMIT 1;")[0]
    
    return fish

def catch_weapon():
    weapon = battle.get_random_weapon()
    user = utility.get_user(session["username"])

    result = utility.general_query("SELECT * FROM weapons WHERE name=? AND owner=?", [weapon['name'], user["id"]])

    if len(result) != 0:
        utility.general_query("UPDATE weapons SET number_owned=number_owned+1 WHERE name=? AND owner=?", [weapon["name"], user['id']])
    else:
        utility.insert_query("weapons", {"name": weapon['name'], "owner": user['id'], "durability": weapon['max_durability']})

    flash(f"You caught a {weapon['name']}!", "success")
    return redirect(url_for('profile_get'))

@bp.get("/")
def fish_get():
    chance = random.randint(1, 100)
    if (chance > 85): # treasure chance: ~15%
        if (chance > 95):
            return catch_weapon()
        else:
            cost = random.randint(40,100)
            utility.general_query("UPDATE profiles SET balance = balance + ? WHERE username=?", [cost, session["username"]])
            flash(f"You caught {cost} gold!","success")
            return redirect(url_for('profile_get'))
    else: # call the database, then send the result to battle
        list = travel.get_current_country_chances(session['username'], utility.species_list).split("%<br>")
        keyset = []
        list.pop()
        for pair in list:
            keyset.append(float(pair.split(": ")[1]))
        fish = get_fish(filter=random.choices(utility.species_list,weights=keyset)[0])
        return redirect(url_for('battle.battle_get', fish=fish["scientific_name"]))