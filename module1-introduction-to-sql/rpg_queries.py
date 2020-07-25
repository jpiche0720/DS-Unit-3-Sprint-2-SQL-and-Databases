import os
import os.path
import sqlite3

# construct a path to wherever your database exists

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "rpg_db.sqlite3")

connection = sqlite3.connect(db_path)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)

q1 = 'How many total Characters are there?'
one = """
SELECT COUNT(name)
FROM charactercreator_character;
"""
q2 = 'How many of each specific subclass?'
two = """
SELECT  (
        SELECT COUNT(*)
        FROM charactercreator_cleric  
        ) AS cleric,
        (
        SELECT COUNT(*)
        FROM   charactercreator_fighter
        ) AS fighter,
        (
        SELECT COUNT(*)
        FROM   charactercreator_mage
        ) AS mage,
        (
        SELECT COUNT(*)
        FROM   charactercreator_necromancer
        ) AS necromancer,
        (
        SELECT COUNT(*)
        FROM   charactercreator_thief
        ) AS thief;
"""
q3 =  'How many total Items?'
three = """
SELECT COUNT(*)
FROM armory_item

"""
q4 = 'How many of the Items are weapons? How many are not?'
four = """
SELECT  (
        SELECT COUNT(*)
        FROM armory_item
        WHERE item_id > 137 and item_id < 175 
        ) AS weapons,
        (
		SELECT COUNT(*)
		FROM armory_item
		WHERE item_id < 138 or item_id > 174
		) AS not_weapons;
"""
q5 = 'How many Items does each character have? (Return first 20 rows)'
five = """
SELECT COUNT(*) AS items
FROM charactercreator_character_inventory 
GROUP BY character_id
ORDER BY character_id
LIMIT 20
"""
q6 = 'How many Weapons does each character have? (Return first 20 rows)'
six = """
SELECT COUNT(*) AS weapons
FROM charactercreator_character_inventory 
WHERE item_id > 137 and item_id < 175
GROUP BY character_id
ORDER BY character_id
LIMIT 20
"""
q7 = 'On average, how many Items does each Character have?'
seven = """
SELECT avg(average_items)
  FROM 
    (
   	SELECT COUNT(*) AS average_items
	FROM charactercreator_character_inventory 
	GROUP BY character_id
	ORDER BY character_id)
"""
q8 = 'On average, how many Weapons does each character have?'
eight = """
SELECT avg(average_items)
  FROM 
    (
   	SELECT COUNT(*) AS average_items
	FROM charactercreator_character_inventory 
	WHERE item_id > 137 and item_id < 175
	GROUP BY character_id
	ORDER BY character_id)
"""
questions = [q1,q2,q3,q4,q5,q6,q7,q8]
queries = [one,two,three,four,five,six,seven,eight]

for i in range(0,8):
    result = cursor.execute(queries[i]).fetchall()
    print(questions[i])
    print(type(result))
    print(result)
    print("-----")
