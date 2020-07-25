import urllib.request, json 

import pandas as pd 



## Get the JSON from Github repo
with urllib.request.urlopen("https://raw.githubusercontent.com/jpiche0720/Django-RPG/master/testdata.json") as url:
    data = json.loads(url.read().decode())

## Get 4 tables into dataframes
characters = []
armory_item = []
armory_weapon = []
others = []
for i in range(0,len(data)):
    in_q = data[i]['model']
    if in_q == 'charactercreator.character':
        characters.append(data[i])
    elif in_q == 'armory.item':
        armory_item.append(data[i])

    elif in_q == 'armory.weapon':
        armory_weapon.append(data[i])
    else:
        others.append(data[i])

# split dictionaries into lists 
character_rows = [] 
character_primkey = []
item_rows = []
item_primkey = []
weapon_rows = []
weapon_primkey = []
types_rows = []
types_primkey = []
names = []

# Create DF
for i in range(0,len(characters)):
    character_row = characters[i]['fields']
    character_pk = characters[i]['pk']
    character_rows.append(character_row)
    character_primkey.append(character_pk)

for i in range(0,len(armory_item)):
    item_row = armory_item[i]['fields']
    item_pk = armory_item[i]['pk']
    item_rows.append(item_row)
    item_primkey.append(item_pk)


for i in range(0,len(armory_weapon)):
    weapon_row = armory_weapon[i]['fields']
    weapon_pk = armory_weapon[i]['pk']
    weapon_rows.append(weapon_row)
    weapon_primkey.append(weapon_pk)

for i in range(0,len(others)):
    name = others[i]['model']
    types_row = others[i]['fields']
    types_pk = others[i]['pk']
    types_rows.append(types_row)
    types_primkey.append(types_pk)
    names.append(name[17:])


# Create primary_key columns for relationships
characters_df = pd.DataFrame(character_rows)
characters_df['primary_key'] = character_primkey
items_df = pd.DataFrame(item_rows)
items_df['primary_key'] = item_primkey
weapons_df = pd.DataFrame(weapon_rows)
weapons_df['primary_key'] = weapon_primkey
types_df = pd.DataFrame(types_rows)
types_df['primary_key'] = types_pk
types_df['type'] = names




if __name__ == '__main__':
    
    # print(characters_df.head())
    # print(items_df.head())
    # print(weapons_df.head())
    # print(types_df.head())


    q1 = 'How many total Characters are there?'
    one = len(characters_df)
    print(q1)
    print(one)
    print('-------')

    q2 = 'How many of each specific subclass?'
    two = types_df['type'].nunique()
    print(q2)
    print(two)
    print('-------')

    q3 =  'How many total Items?'
    three = len(items_df)
    print(q3)
    print(three)
    print('-------')

    
    q4 = 'How many of the Items are weapons? How many are not?'
    weapon_identifier = weapons_df['primary_key'].to_list()
    low = min(weapon_identifier)
    are_weapons = len(items_df[items_df['primary_key'] >= min(weapon_identifier)])
    not_weapons = len(items_df[items_df['primary_key'] < min(weapon_identifier)])
    print(q4)
    print(are_weapons,not_weapons)
    print('-------')
    

    q5 = 'How many Items does each character have? (Return first 20 rows)'
    num_items = []
    for i in range(0,len(types_df)):
        num = len(types_df['inventory'][i])
        num_items.append(num)
    print(q5)
    print(num_items[:20])
    print('-------')

    q6 = 'How many Weapons does each character have? (Return first 20 rows)'
    num_of_weapons = []
    for i in range(0,len(characters_df)):
        in_q = characters_df['inventory'][i] 
        for num in in_q:
            weapons = []
            if num in weapon_identifier:
                weapons.append(1)
            else:
                weapons.append(0)
            num_of_weapons.append(sum(weapons))
    
    print(q6)
    print(num_of_weapons[0:20])
    print('-------')
    


    q7 = 'On average, how many Items does each Character have?'
    print(q7)
    num_of_items = []
    for i in range(0,len(characters_df)):
        in_q = len(characters_df['inventory'][i])
        num_of_items.append(in_q)

    print(sum(num_of_items)/len(num_of_items))

    q8 = 'On average, how many Weapons does each character have?'
    print(q8)
    print(sum(num_of_weapons)/len(num_of_weapons))
    print('-------')



# How many total Characters are there?
# 302
# -------
# How many of each specific subclass?
# 5
# -------
# How many total Items?
# 174
# -------
# How many of the Items are weapons? How many are not?
# 37 137
# -------
# How many Items does each character have? (Return first 20 rows)
# [3, 3, 2, 4, 4, 1, 5, 3, 4, 4, 3, 3, 4, 4, 4, 1, 5, 5, 3, 1]
# -------
# How many Weapons does each character have? (Return first 20 rows)
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
# -------
# On average, how many Items does each Character have?
# 2.9735099337748343
# On average, how many Weapons does each character have?
# 0.22605790645879734
# -------
