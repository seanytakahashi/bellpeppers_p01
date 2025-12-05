import urllib.request
import urllib.parse
import json
from flask import Flask

key = "GER" # CHANGEABLE. THIS IS A TEST CASE.
url = "https://restcountries.com/v3.1/alpha/" + key

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())


common = data[0]['name']['common']

print(common)

# if __name__ == '__main__':
#     app.run(debug=True)
