# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.get('/signup')
def signup_get():
    return render_template('auth/signup.html')

@bp.post('/signup')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    #check if username exist

    hashed_pswd = generate_password_hash(password)

    #add info to db

    flash('Signup successful!')
    return redirect(url_for('auth/login_get'))

@bp.get('/login')
def login_get():
    return render_template('auth/login.html')

@bp.post('/login')
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    # check for username and pswd
