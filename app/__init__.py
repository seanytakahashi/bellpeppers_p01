# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Flask, render_template, request, flash, url_for, redirect, session
import utility
import random
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
    if 'username' not in session.keys() and request.blueprint != 'auth' and request.path != '/':
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

    fish = utility.general_query("SELECT * FROM fish WHERE owner=?;", [user["id"]])
    weapons = utility.general_query("SELECT name FROM weapons WHERE owner=?;", [user["id"]])

    for single_fish in fish:
        stats = battle.initialize_fish(single_fish["scientific_name"])
        for key in stats:
            single_fish[key] = stats[key]

    for i in range(len(weapons)):
        weapons[i] = battle.initialize_weapon(weapons[i]["name"], user["id"])

    return render_template('profile.html', user=user, all_fish_owned=fish, all_weapons_owned=weapons)

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

    random_fish = utility.general_query("SELECT * FROM fish WHERE owner=? AND number_owned>0 ORDER BY random() LIMIT 6", [user['id']])
    fish_stats = []
    
    for fish in random_fish:
        data = battle.initialize_fish(fish["scientific_name"])

        fish["price"] = int((data["max_health"] + data["accuracy"]) / 2)

        # 0 index: fish data including health and accuracy; 1 index: number owned; 2 index: price
        fish_stats.append([data, fish["number_owned"], fish["price"]])


    weapons = utility.query_cache("SELECT * FROM weapons ORDER BY random() LIMIT 6")
    for weapon in weapons:
        weapon["price"] = weapon["accuracy"] + weapon["max_durability"]

    return render_template('shop.html', weapons=weapons, random_fish=fish_stats, user=user)

@app.post('/sell_fish')
def sell_fish():
    user = utility.get_user(session["username"])
    
    fish_sold = request.form.get('fish_name')
    fish_price = request.form.get('fish_price')

    utility.general_query("UPDATE profiles SET balance=balance+? WHERE username=?", [fish_price, session["username"]])
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

@app.get('/inject')
def cheat_homepage():
  return render_template('inject.html', user=utility.get_user(session['username']))

@app.post('/inject_currency')
def inject_money():
  cost = request.form.get('amount')
  print(cost)
  utility.general_query("UPDATE profiles SET balance=balance+? WHERE username=?", [cost, session["username"]])
  flash(f"Gained {cost} gold.", "success")
  return redirect(url_for("cheat_homepage"))

@app.post('/inject_weapon')
def inject_weapon():
  user = utility.get_user(session["username"])
  weapon = utility.query_cache("SELECT * FROM weapons ORDER BY random() LIMIT 1")[0]
  result = utility.general_query("SELECT * FROM weapons WHERE name=? AND owner=?", [weapon['name'], user["id"]])
  if len(result) != 0:
      utility.general_query("UPDATE weapons SET number_owned=number_owned+1 WHERE name=? AND owner=?", [weapon["name"], user['id']])
  else:
      utility.insert_query("weapons", {"name": weapon['name'], "owner": user['id'], "durability": weapon['max_durability']})
  flash(f"Added {weapon['name']} to inventory.", "success")
  return redirect(url_for("cheat_homepage"))

@app.post('/force_encounter')
def force_encounter():
  filter = request.form.get('type')
  print(filter)
  print(filter)
  print(filter)
  print(filter)
  print(filter)
  print(filter)
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
      ("filter", f"/species@status in ('{filter}')"),
  ])["data"]

  for fish in fishSet:
      fish[3] = utility.find_area(fish[3][9:-2])
  
  raw = random.choice(fishSet)
  fish = {
      "scientific_name": raw[1]["value"],
      "common_name": raw[0],
      "status": raw[2],
      "accuracy": max(60,min(100, raw[3])),
      "type": raw[4]
  }
  utility.cache_entry("fish", fish)
  return redirect(url_for('battle.battle_get', fish=fish["scientific_name"]))
  
if __name__ == '__main__':
    app.run(debug=True)
