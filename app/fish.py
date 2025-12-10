# Sean Takahashi, Ivan Chen, James Lei, Eviss Wu
# Bell Peppers
# SoftDev
# P01
# 2025-12-22m

import utility
import random

def get_fish():
    fishSet = utility.call_api("Species", "/export", [
        ("format", "json"),
        ("columns", "/species@cn,sn,status,range_envelope,gn"),
        ("sort", "/species@cn asc;/species@sn asc"),
        ("filter", "/species@status not in ('Experimental Population, Non-Essential')"),
        ("filter", "/species@range_envelope is not null")
    ])["data"]
    # x = 0
    for fish in fishSet:
        # x += 1
        try:
            fish[3] = utility.find_area(fish[3][9:-2])
        except:
            print(fish[0])
            print(fish[3])
    # print(x)
    return random.choice(fishSet)
