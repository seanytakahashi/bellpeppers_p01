# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Flask, render_template, request, flash, url_for, redirect, session
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
    elif 'username' in session.keys():
        user = utility.get_user(session['username'])
        if user is None:
            session.pop('username', None)
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
    accordion_data = parse_chance_list(user, utility.species_list)
    print(f"DEBUG: accordion_data = {accordion_data}")
    current_country_chances = get_current_country_chances(user, utility.species_list)
    return render_template(
        'travel.html',
        accordion_data=accordion_data,
        current_country_chances=current_country_chances
    )

@app.post('/travel')
def travel_post():
    user = session["username"]
    new_country_code = request.form["country"]
    utility.general_query("UPDATE profiles SET country=? WHERE username=?", [new_country_code, user])
    country_name = request.form.get("country_name", new_country_code)
    flash(f"You have traveled to {country_name}!", "success")
    return redirect(url_for("profile_get"))

@app.get('/shop')
def shop_get():
    user = utility.get_user(session["username"])

    random_fish = utility.general_query("SELECT * FROM fish WHERE owner=? ORDER BY random() LIMIT 6", [user['id']])
    fish_stats = []
    
    for fish in random_fish:
        raw = utility.pull_cache("fish", ("scientific_name", fish["scientific_name"]))

        data = battle.initialize_fish(raw)

        fish["price"] = int((data["stats"]["max_health"] + data["stats"]["accuracy"]) / 2)

        # 0 index: fish data including health and accuracy; 1 index: number owned; 2 index: price
        fish_stats.append([data, fish["number_owned"], fish["price"]])


    weapons = utility.query_cache("SELECT * FROM weapons ORDER BY random() LIMIT 6")
    for weapon in weapons:
        weapon["price"] = weapon["range"] + weapon["max_durability"]

    return render_template('shop.html', weapons=weapons, random_fish=fish_stats, user=user)

@app.post('/sell_fish')
def sell_fish():
    user = utility.get_user(session["username"])
    
    fish_sold = request.form.get('fish_name')
    fish_price = request.form.get('fish_price')

    utility.general_query("UPDATE profiles SET balance=balance+? WHERE username=?", [fish_price, session["username"]])

    number_owned = utility.general_query("SELECT number_owned FROM fish WHERE scientific_name=? AND owner=?", [fish_sold, user['id']])
    if number_owned[0]['number_owned'] == 1:
        utility.general_query("DELETE FROM fish WHERE scientific_name=? AND owner=?", [fish_sold, user['id']])
    else:
        utility.general_query("UPDATE fish SET number_owned=number_owned-1 WHERE scientific_name=? AND owner=?", [fish_sold, user['id']])
    
    return redirect(url_for('shop_get'))

@app.post('/buy_weapon')
def buy_weapon():
    user = utility.get_user(session["username"])

    if "weapon_name" in request.form:
        weapon_bought = request.form.get('weapon_name')
        weapon_price = request.form.get('weapon_price')

        weapon = utility.pull_cache("weapons", ("name", weapon_bought))
        
        utility.general_query("UPDATE profiles SET balance=balance-? WHERE rowid=?", [weapon_price, user['id']])

        result = utility.general_query("SELECT * FROM weapons WHERE name=? AND owner=?", [weapon['name'], user["id"]])
        if len(result) != 0:
            utility.general_query("UPDATE weapons SET number_owned=number_owned+1 WHERE name=? AND owner=?", [weapon["name"], user['id']])
        else:
            utility.insert_query("weapons", {"name": weapon['name'], "owner": user['id'], "durability": weapon['max_durability']})

    return redirect(url_for('shop_get'))

if __name__ == '__main__':
    app.run(debug=True)
