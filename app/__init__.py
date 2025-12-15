# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3
import utility

app = Flask(__name__)
app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"

import auth
app.register_blueprint(auth.bp)
import battle
app.register_blueprint(battle.bp)
import fish
app.register_blueprint(fish.bp)

@app.get('/')
def home_get():
    return render_template('base.html')

@app.get('/profile')
def profile_get():
    user = utility.get_user(session["username"])

    all_fish_owned = utility.general_query("SELECT common_name, number_owned FROM fish WHERE owner=?;", [user["id"]])
    all_weapons_owned = utility.general_query("SELECT name, durability FROM weapons WHERE owner=?;", [user["id"]])
    print(all_weapons_owned)

    return render_template('profile.html', user=user, all_fish_owned=all_fish_owned, all_weapons_owned=all_weapons_owned)

@app.post('/profile')
def profile_post():
    weapon_equip = request.form.get('Equip')
    user = session['username']
    utility.general_query("UPDATE profiles SET equipped_weapon=? WHERE username=?", [weapon_equip, user])

# Display possible travel locations
@app.get('/travel')
def travel_get():
    return ""

@app.post('/travel')
def travel_post():
    return ""

if __name__ == '__main__':
    app.run(debug=True)
