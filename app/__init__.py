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

@app.get('/')
def home_get():
    return render_template('base.html')

@app.get('/profile')
def profile_get():
    user = session['username']
    user_info = utility.general_query("SELECT country, balance, id, equipped_weapon, health FROM profiles WHERE username = ?;", [user])
    user_country, user_balance, user_id, weapon, health = user_info[0]

    all_fish_owned = utility.general_query("SELECT common_name, number_owned FROM fish WHERE owner = ?;", [user_id])
    all_weapons_owned = utility.general_query("SELECT name, durability FROM weapons WHERE owner = ?;", [user_id])

    return render_template('profile.html', current_user=user, country=user_country, balance=user_balance, all_fish=all_fish_owned, all_weapons=all_weapons_owned, user_weapon = weapon, user_health = health)

# Display possible travel locations
@app.get('/travel')
def travel_get():
    return ""

@app.post('/travel')
def travel_post():
    return ""

if __name__ == '__main__':
    app.run(debug=True)
