# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

bp = Blueprint('battle', __name__, url_prefix='/battle')

import utility

@bp.get('/')
def battle_get():
    return render_template("battle.html")
