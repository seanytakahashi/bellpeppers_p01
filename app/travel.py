import utility

def get_common(key):
    data = utility.call_api("Countries", "/alpha/" + key)
    common = data[0]['name']['common']
    return common

def get_pop(key):
    data = utility.call_api("Countries", "/alpha/" + key)
    pop = data[0]['population']
    return pop

def get_list(user):
    user_data = utility.get_user(user)
    country_code = user_data["country"]
    data = utility.call_api("Countries", "/alpha/" + country_code)
    borders = data[0].get('borders', [])
    return borders

def get_common_list(user):
    list = []
    for country_code in get_list(user):
        list.append(get_common(country_code))
    return list

def get_pop_list(user):
    list = []
    for country_code in get_list(user):
        list.append(get_pop(country_code))
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
    result = []
    country_codes = get_list(user)
    
    if not country_codes:
        return []
    
    chances_list = get_chance_list(user)
    
    for i in range(len(country_codes)):
        cstring = ""
        for j, chance in enumerate(chances_list[i]):
            cstring += species_list[j] + ": " + str(round(chance, 2)) + "%<br>"
        
        country_code = country_codes[i]
        country_name = get_common(country_code)
        result.append((cstring, country_code, country_name))
    
    return result

def get_current_country_chances(user, species_list):
    country_code = utility.get_user(user)["country"]
    chances = make_numbers(get_pop(country_code))
    cstring = ""
    for i, chance in enumerate(chances):
        cstring += species_list[i] + ": " + str(round(chance, 2)) + "%<br>"
    return cstring
