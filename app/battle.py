# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utility import call_api, cache_entry
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

def parse_fish():
    raw = get_fish()
    fish = {
        "scientific_name": raw[1]["value"],
        "common_name": raw[0],
        "status": raw[2],
        "range": raw[3],
        "type": raw[4]
    }
    cache_entry("fish", fish)
    return fish

@bp.get('/')
def battle_get():
    weapon = get_random_weapon()
    fish = parse_fish()

    print(weapon)
    print(fish)

    return render_template("battle.html", fish=fish, weapon=weapon)

# print(get_random_weapon())
