import utility

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

def make_numbers(p):
    nums = []
    current = p
    for times in range(13):
        current = (current * 1103515245 + 12345) % 2**31
        nums.append((current % 1000000) / 1000000)
    total = sum(nums)
    scale = 100 / total
    return [n * scale for n in nums]

def get_chance_list():
    list = []
    for pop in get_pop_list():
        list.append(make_numbers(pop))
    return list
