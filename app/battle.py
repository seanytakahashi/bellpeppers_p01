# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utility import call_api
import random

bp = Blueprint('battle', __name__, url_prefix='/battle')

def get_random_weapon():
    allWeapons = call_api("Dnd", "/api/2014/equipment-categories/simple-weapons")["equipment"]
    weapon = call_api("Dnd", random.choice(allWeapons)["url"])
    return weapon

@bp.get('/')
def battle_get():
    return render_template("battle.html")

print(get_random_weapon())