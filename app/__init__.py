# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

# Imports
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*"

import auth
app.register_blueprint(auth.bp)

import utility

@app.context_processor
def user_context(): # persistent info made avalible for all html templates
    return {
        "logged_in": 'username' in session,
        "current_user": session.get('username')
    }

@app.get('/')
def home_get():
    return render_template('base.html')

@app.get('/profile')
def profile_get():
    user = session['username']
    user_info = utility.general_query("SELECT country, balance FROM profiles WHERE username = ?;", [user])
    user_country, user_balance = user_info[0]
    return render_template('profile.html', country=user_country, balance=user_balance)

# Display possible travel locations
@app.get('/travel')
def travel_get():
    return ""

@app.post('/travel')
def travel_post():
    return ""

if __name__ == '__main__':
    app.run()
