# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import utility
import random

bp = Blueprint('battle', __name__, url_prefix='/battle')

def roll_dice(dice):
    dice = dice.split("d")
    output = 0
    for i in range(int(dice[0])):
        output += random.randint(1, int(dice[1]))
    return output

def get_random_weapon():
    all_weapons = utility.call_api("Dnd", "/api/2014/equipment-categories/simple-weapons")["equipment"]
    raw = utility.call_api("Dnd", random.choice(all_weapons)["url"])

    weapon = {
        "name": raw["name"],
        "damage_dice": raw["damage"]["damage_dice"],
        "damage_type": raw["damage"]["damage_type"]["name"],
        "max_durability": max(raw["weight"], 1) * 10,
        "range": raw["range"]["normal"]
    }

    utility.cache_entry("weapons", weapon)
    return weapon

def get_fish_stats(status):
    stats = {
        "Resolved Taxon": {
            "max_health": 10,
            "damage": "1d4",
        },
        "Species of Concern": {
            "max_health": 20,
            "damage": "1d4",
        },
        "Threatened": {
            "max_health": 25,
            "damage": "1d6",
        },
        "Endangered": {
            "max_health": 30,
            "damage": "1d8",
        },
        "Extinction": {
            "max_health": 30,
            "damage": "2d10"
        }
    }
    return stats[status]

def initialize_fish(fish):
    fish["stats"] = get_fish_stats(fish["status"])
    fish["stats"]["health"] = fish["stats"]["max_health"]

    fish["stats"]["accuracy"] = min(100, fish["range"])
    del fish["range"]

    return fish

def initialize_weapon(name, user):
    item = utility.general_query("SELECT * FROM weapons WHERE name=? AND owner=?", [name, user])[0]
    weapon = utility.pull_cache("weapons", ("name", name))

    weapon["durability"] = item['durability']
    weapon["number_owned"] = item["number_owned"]
    weapon["accuracy"] = min(100, weapon["range"] * 10)
    del weapon["range"]

    return weapon

@bp.get('/')
def battle_get():
    scientific_name = request.args["fish"]
    raw = utility.pull_cache("fish", ("scientific_name", scientific_name))
    fish = initialize_fish(raw)

    user = utility.get_user(session['username'])

    session["battle_log"] = [("You're starting a battle!", "success")]

    if (user['equipped_weapon'] == None):
        flash("You don't have a weapon equipped and you fled the battle!", "danger")
        return redirect(url_for("profile_get"))

    weapon = initialize_weapon(user['equipped_weapon'], user["id"])

    return render_template("battle.html", fish=fish, weapon=weapon, user=user)

@bp.post('/')
def battle_post():
    scientific_name = request.form["fish_species"]
    raw = utility.pull_cache("fish", ("scientific_name", scientific_name))
    fish = initialize_fish(raw)
    fish["stats"]["health"] = int(request.form["fish_health"])

    user = utility.get_user(session['username'])
    weapon = initialize_weapon(user['equipped_weapon'], user["id"])

    print(weapon)
    print(fish)
    print(user)
    print(session["battle_log"])

    # Decrease durability
    weapon["durability"] -= 1
    if (weapon["durability"] == 0):
        if (weapon["number_owned"] == 1):
            flash("Your weapon broke and you fled the battle!", "danger")
            utility.general_query("UPDATE profiles SET equipped_weapon=NULL WHERE id=?", [user["id"]])
            utility.general_query("DELETE FROM weapons WHERE name=? AND owner=?", [weapon["name"], user["id"]])
            return redirect(url_for('profile_get'))
        else:
            weapon["number_owned"] -= 1
            utility.general_query("UPDATE weapons SET number_owned=number_owned-1, durability=? WHERE name=? AND owner=?", [weapon["max_durability"], weapon["name"], user["id"]])
    else:
        utility.general_query("UPDATE weapons SET durability=durability-1 WHERE name=? AND owner=?", [weapon["name"], user["id"]])

    # Player attacks

    miss = random.randint(0, 100) > weapon['accuracy']
    if miss:
        session["battle_log"].append(("You tried to attack but failed!", "warning"))
    else:
        damage_dice = weapon["damage_dice"]
        damage = roll_dice(damage_dice)

        if fish["stats"]["health"] <= damage:
            existing = utility.general_query("SELECT * FROM fish WHERE owner=? AND scientific_name=?", [user["id"], fish["scientific_name"]])
            if len(existing) > 0:
                utility.general_query("UPDATE fish SET number_caught=number_caught+1, number_owned=number_owned+1 WHERE scientific_name=? AND owner=?", [fish["scientific_name"], user["id"]])
            else:
                utility.insert_query("fish", {"scientific_name": fish["scientific_name"], "owner": user["id"]})

            flash("You won the battle and caught this fish!", "success")
            return redirect(url_for("profile_get"))

        fish["stats"]["health"] -= damage
        session["battle_log"].append((f"You attacked for {damage} damage!", "success"))

    # Fish attacks
    miss = random.randint(0, 100) > fish['stats']['accuracy']
    if miss:
        session["battle_log"].append(("The fish tried to attack you but missed!", "warning"))
    else:
        damage_dice = fish["stats"]["damage"]
        damage = roll_dice(damage_dice)

        if user["health"] <= damage:
            utility.general_query("UPDATE profiles SET balance=balance-50, health=100 WHERE username=?", [session["username"]])
            flash("You died and had to pay 50 coins to recover!", "danger")
            return redirect(url_for("profile_get"))

        utility.general_query("UPDATE profiles SET health=health-? WHERE username=?", [damage, session["username"]])

        user["health"] -= damage
        session["battle_log"].append((f"You were attacked for {damage} damage!", "danger"))

    flash("")
    return render_template("battle.html", fish=fish, weapon=weapon, user=user)

# print(get_random_weapon())
