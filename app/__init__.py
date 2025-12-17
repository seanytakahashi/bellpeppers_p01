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
from battle import *
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
    return render_template('base.html')

@app.get('/profile')
def profile_get():
    user = utility.get_user(session["username"])

    all_fish_owned = utility.general_query("SELECT scientific_name, number_owned FROM fish WHERE owner=?;", [user["id"]])
    all_weapons_owned = utility.general_query("SELECT name, number_owned, durability FROM weapons WHERE owner=?;", [user["id"]])

    #

    return render_template('profile.html', user=user, all_fish_owned=all_fish_owned, all_weapons_owned=all_weapons_owned)

@app.post('/profile')
def profile_post():
    weapon_equip = request.form.get('weapon')
    user = session['username']
    utility.general_query("UPDATE profiles SET equipped_weapon=? WHERE username=?", [weapon_equip, user])

    return redirect(url_for('profile_get'))

# Display possible travel locations
@app.get('/travel')
def travel_get():
    accordion_titles = getPopList()
    accordion_contents = parseChanceList()
    accordion_data = zip(accordion_titles, accordion_contents)
    return render_template_string(HTML_TEMPLATE, accordion_data=accordion_data)

@app.post('/travel')
def travel_post():
    return ""



if __name__ == '__main__':
    app.run(debug=True)
