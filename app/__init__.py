# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3
import utility
from travel import *

app = Flask(__name__)
app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"

import auth
app.register_blueprint(auth.bp)
import battle
app.register_blueprint(battle.bp)
import fish
app.register_blueprint(fish.bp)

@app.before_request
def check_authentification():
    if 'username' not in session.keys() and request.blueprint != 'auth':
        flash("Please log in to view our website", "danger")
        return redirect(url_for("auth.login_get"))

@app.get('/')
def home_get():
    return render_template('home.html')

@app.get('/profile')
def profile_get():
    user = utility.get_user(session["username"])

    all_fish_owned = utility.general_query("SELECT scientific_name, number_owned FROM fish WHERE owner=?;", [user["id"]])
    all_weapons_owned = utility.general_query("SELECT name FROM weapons WHERE owner=?;", [user["id"]])

    fish_stats = []
    weapons_stats = []

    for fish in all_fish_owned:
        raw = utility.pull_cache("fish", ("scientific_name", fish["scientific_name"]))
        # 0 index: fish data including health and accuracy; 1 index: number owned
        fish_stats.append([battle.initialize_fish(raw), fish["number_owned"]])

    for weapon in all_weapons_owned:
        weapons_stats.append(battle.initialize_weapon(weapon["name"], user["id"]))

    return render_template('profile.html', user=user, all_fish_owned=fish_stats, all_weapons_owned=weapons_stats)

@app.post('/profile')
def profile_post():
    weapon_equip = request.form.get('weapon')
    user = session['username']
    utility.general_query("UPDATE profiles SET equipped_weapon=? WHERE username=?", [weapon_equip, user])

    return redirect(url_for('profile_get'))

# Display possible travel locations
@app.get('/travel')
def travel_get():
    user = session["username"]

    accordion_titles = get_common_list(user)
    accordion_contents = parse_chance_list(user, utility.species_list)
    accordion_data = zip(accordion_titles, accordion_contents)

    current_country_chances = get_current_country_chances(user, utility.species_list)

    return render_template(
        'travel.html',
        accordion_data=accordion_data,
        current_country_chances=current_country_chances
    )

@app.get('/shop')
def shop_get():
    weapons = utility.query_cache("SELECT * FROM weapons ORDER BY random() LIMIT 6")

    for weapon in weapons:
        weapon["price"] = weapon["range"] + weapon["max_durability"]

    print(weapons[0])

    return render_template('shop.html', weapons=weapons)

if __name__ == '__main__':
    app.run(debug=True)
