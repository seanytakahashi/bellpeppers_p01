import utility

def get_common(key):
    data = utility.call_api("Countries", "/" + key)
    common = data[0]['name']['common']
    return common

def get_pop(key):
    data = utility.call_api("Countries", "/" + key)
    pop = data[0]['maps']['population']
    return pop

def get_list(username):
    country = utility.get_user(username)
    data = utility.call_api("Countries", "/" + country)
    list = data[0]['borders']
    return list

def get_common_list():
    list = []
    for country in get_list():
        list.append(get_common(country))
    return list

def get_pop_list():
    list = []
    for country in get_list():
        list.append(get_pop_list(country))
    return list

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
