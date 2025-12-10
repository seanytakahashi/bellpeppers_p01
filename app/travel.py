import urllib.request
import urllib.parse
import json
from flask import Flask

def getCommon(key):
    url = "https://restcountries.com/v3.1/alpha/" + key
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    common = data[0]['name']['common']
    #print(common)
    return(common)

def getPop(key):
    url = "https://restcountries.com/v3.1/alpha/" + key
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    pop = data[0]['maps']['population']
    #print(pop)
    return(pop)

def getList():
    url = "https://restcountries.com/v3.1/alpha/" + curKey
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    list = data[0]['borders']
    #print(list)
    return(list)

def getCommonList():
    list = []
    for country in getList():
        list.append(getCommon(country));
    #print(list)
    return list

def getPopList():
    list = []
    for country in getList():
        list.append(getPop(country));
    #print(list)
    return list

def make_numbers(p):
    nums = []
    current = p

    for times in range(15):
        current = (current * 1103515245 + 12345) % 2**31
        nums.append((current % 1000000) / 1000000)
    total = sum(nums)
    scale = 100 / total
    return [n * scale for n in nums]

def getChanceList():
    list = []
    for pop in getPopList():
        list.append(make_numbers(pop));
    #print(list)
    return list
