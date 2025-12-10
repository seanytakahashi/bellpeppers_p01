# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

import utility
import random

def get_fish():
    fishSet = utility.call_api("Species", "/export", {
        "format": "json",
        "columns": "/species@cn,sn,status,range_envelope,gn",
        "sort": "/species@cn asc;/species@sn asc",
        "filter": "/species@range_envelope is not null",
        "filter": "/species@status not in ('Experimental Population, Non-Essential')"
    })["data"]
    return random.choice(fishSet)
