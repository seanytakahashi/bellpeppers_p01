import urllib.request
import urllib.parse
import json
from flask import Flask

curKey = 'GER'

def getCommon(key):
    url = "https://restcountries.com/v3.1/alpha/" + key
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    common = data[0]['name']['common']
    #print(common)
    return(common)

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

getCommonList()

# if __name__ == '__main__':
#     app.run(debug=True)
