import pandas as pd 
import sqlite3

dfpath = 'buddymove_holidayiq.csv'
df = pd.read_csv(dfpath)
print(df.head)

sqlbase = df.to_sql('buddymove_dataset',sqlite3.Connection('buddymove_holidayiq.sqlite3'),if_exists = 'replace')

connection = sqlite3.connect('buddymove_holidayiq.sqlite3')
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)



q1 = 'Count how many rows you have - it should be 249!'
one = """
SELECT COUNT(*)
FROM buddymove_dataset
"""
q2 = 'How many users who reviewed at least 100 Nature in the category also reviewed at least 100 in the Shopping category?'
two = """
SELECT COUNT(*)
FROM buddymove_dataset
WHERE Nature > 99 and Shopping > 99
"""
q3 = '(Stretch) What are the average number of reviews for each category?'
three = """
SELECT  (
        SELECT AVG(Sports)
        FROM buddymove_dataset
        ) AS sports,
        (
        SELECT AVG(Religious)
        FROM   buddymove_dataset
        ) AS religious,
        (
        SELECT AVG(Nature)
        FROM   buddymove_dataset
        ) AS nature,
        (
        SELECT AVG(Theatre)
        FROM   buddymove_dataset
        ) AS theatre,
        (
        SELECT AVG(Shopping)
        FROM   buddymove_dataset
        ) AS shopping,
        (
        SELECT AVG(Picnic)
        FROM   buddymove_dataset
        ) AS picnic;
"""

questions = [q1,q2,q3]
queries = [one,two,three]

for i in range(0,3):
    result = cursor.execute(queries[i]).fetchall()
    print(questions[i])
    print(type(result))
    print(result)
    print("-----")