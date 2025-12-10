# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

import utility

@bp.get('/signup')
def signup_get():
    return render_template('signup.html')

@bp.post('/signup')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    #check if username exist
    row = utility.general_query("SELECT username FROM profiles WHERE username = ?", [username])
    if not row:
        hashed_pswd = generate_password_hash(password)
        utility.insert_query("profiles", ({"username": username, "password": hashed_pswd}))
        flash('Signup successful!', 'success')
        return redirect(url_for('auth.login_get'))
    else:
        flash("Username already taken!", 'danger')
        return redirect(url_for('auth.signup_get'))

@bp.get('/logout')
def logout_get():
    session.pop('username', None)
    flash("Logout successful!", 'success')
    return render_template('login.html')

@bp.get('/login')
def login_get():
    return render_template('login.html')

@bp.post('/login')
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    # check for username and pswd
    row = utility.general_query("SELECT password FROM profiles WHERE username = ?", [username])

    if not row:
        flash('Error: Username or password incorrect', 'danger')
        return redirect(url_for('auth.login_get'))
    elif check_password_hash(row[0][0], password):
        flash('Login successful!', 'success')
        session['username'] = username
        return redirect(url_for('home_get'))
    else:
        flash('Error: Username or password incorrect', 'danger')
        return redirect(url_for('auth.login_get'))
