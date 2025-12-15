# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utility import *
from fish import get_fish
import random

bp = Blueprint('battle', __name__, url_prefix='/battle')

def get_random_weapon():
    all_weapons = call_api("Dnd", "/api/2014/equipment-categories/simple-weapons")["equipment"]
    raw = call_api("Dnd", random.choice(all_weapons)["url"])

    weapon = {
        "name": raw["name"],
        "damage_dice": raw["damage"]["damage_dice"],
        "damage_type": raw["damage"]["damage_type"]["name"],
        "max_durability": raw["weight"] * 10,
        "range": raw["range"]["normal"]
    }

    cache_entry("weapons", weapon)
    return weapon

def get_fish_stats(status):
    stats = {
        "Resolved Taxon": {
            "max_health": 5,
            "damage": "1d4",
        },
        "Species of Concern": {
            "max_health": 8,
            "damage": "1d4",
        },
        "Threatened": {
            "max_health": 10,
            "damage": "1d4",
        },
        "Endangered": {
            "max_health": 10,
            "damage": "1d8",
        },
        "Extinction": {
            "max_health": 30,
            "damage": "2d10"
        }
    }
    return stats[status]

def parse_fish():
    raw = get_fish()
    fish["stats"] = get_fish_stats(fish["status"])
    fish["stats"]["accuracy"] = fish["range"]
    del fish["range"]
    fish["stats"]["health"] = fish["stats"]["max_health"] - 2
    return fish

def parse_weapon(name, user):
    item = general_query("SELECT * FROM weapons WHERE name=? AND owner=?", [name, user])[0]
    weapon = pull_cache("weapons", ("name", name))
    weapon["durability"] = item['durability']
    weapon["accuracy"] = weapon["range"] * 10
    del weapon["range"]
    return weapon

@bp.get('/')
def battle_get():
    fish = parse_fish()
    user = get_user(session['username'])
    weapon = parse_weapon(user['equipped_weapon'], user["id"])

    return render_template("battle.html", fish=fish, weapon=weapon, user=user)

@bp.post('/')
def battle_post():
    fish = parse_fish()
    user = get_user(session['username'])
    weapon = parse_weapon(user['equipped_weapon'], user["id"])
    return render_template("battle.html", fish=fish, weapon=weapon, user=user)

# print(get_random_weapon())
