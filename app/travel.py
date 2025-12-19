import utility

def get_common(key):
    data = utility.call_api("Countries", "/name/" + key)
    common = data[0]['name']['common']
    return common

def get_pop(key):
    data = utility.call_api("Countries", "/name/" + key)
    pop = data[0]['population']
    return pop

def get_list(user):
    country = utility.get_user(user)["country"]
    data = utility.call_api("Countries", "/name/" + country)
    borders = data[0].get('borders', [])
    return borders

def get_common_list(user):
    list = []
    for country in get_list(user):
        list.append(get_common(country))
    return list

def get_pop_list(user):
    list = []
    for country in get_list(user):
        list.append(get_pop(country))
    return list

def make_numbers(p):
    nums = []
    current = p
    for times in range(13):
        current = (current * 1103515245 + 12345) % 2**31
        nums.append((current % 1000000) / 1000000)
    total = sum(nums)
    if total == 0:
        return [0] * 13
    scale = 100 / total
    return [n * scale for n in nums]

def get_chance_list(user):
    list = []
    for pop in get_pop_list(user):
        list.append(make_numbers(pop))
    return list

def parse_chance_list(user, species_list):
    content = []
    for chances in get_chance_list(user):
        cstring = ""
        for i, chance in enumerate(chances):
            cstring += species_list[i] + ": " + str(round(chance, 2)) + "%<br>"
        content.append(cstring)
    return content

def get_current_country_chances(user, species_list):
    country = utility.get_user(user)["country"]
    chances = make_numbers(get_pop(country))
    cstring = ""
    for i, chance in enumerate(chances):
        cstring += species_list[i] + ": " + str(round(chance, 2)) + "%<br>"
    return cstring
