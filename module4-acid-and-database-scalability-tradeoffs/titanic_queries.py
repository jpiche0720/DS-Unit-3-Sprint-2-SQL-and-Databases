import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

CSV_FILEPATH = 'module2-sql-for-analysis/titanic.csv'
load_dotenv() #> loads contents of the .env file into the script's environment

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR:", cursor)


q1 = 'How many passengers survived, and how many died?'
Q1 = '''
SELECT
(SELECT COUNT(*)
FROM passengers
WHERE survived = 0) AS Fatalities,
(SELECT COUNT(*)
FROM passengers
WHERE survived = 1) AS Survivors;
'''




q2 = 'How many passengers were in each class?'
Q2 = '''
SELECT
(SELECT COUNT(*)
FROM passengers
WHERE pclass = 1) AS First_class,

(SELECT COUNT(*)
FROM passengers
WHERE pclass = 2) AS Second_class,

(SELECT COUNT(*)
FROM passengers
WHERE pclass = 3) AS Third_class;

'''



q3 =  'How many passengers survived/died within each class'
Q3 = '''
SELECT  
(SELECT COUNT(*)
FROM passengers
WHERE pclass = 1 and survived = 0) AS First_class_fatality,

(SELECT COUNT(*)
FROM passengers
WHERE pclass = 1 and survived = 1) AS First_class_survivors,
    
(SELECT COUNT(*)
FROM passengers
WHERE pclass = 2 and survived = 0) AS Second_class_fatality,

(SELECT COUNT(*)
FROM passengers
WHERE pclass = 2 and survived = 1) AS Second_class_survivors,

(SELECT COUNT(*)
FROM passengers
WHERE pclass = 3 and survived = 0) AS Third_class_fatality,
    
(SELECT COUNT(*)
FROM passengers
WHERE pclass = 3 and survived = 1) AS Third_class_survivors;           

   
'''



q4 = 'What was the average age of survivors vs nonsurvivors?'
Q4 = '''
SELECT  
(SELECT AVG(age)
FROM passengers
WHERE survived = 0) AS Age_Fatalities,

(SELECT AVG(age)
FROM passengers
WHERE survived = 1) AS Age_Survivors;
'''
q5 = 'What was the average age of each passenger class?'
Q5 = '''
SELECT 
(SELECT AVG(age)
FROM passengers
WHERE pclass = 1) AS Age_First_class,
            
(SELECT AVG(age)
FROM passengers
WHERE pclass = 2
) AS Age_Second_class,
            
(SELECT AVG(age)
FROM passengers
WHERE pclass = 3
) AS Age_Third_class;
'''

q6 = 'What was the average fare by passenger class? By survival?'
Q6 = '''
SELECT  
(SELECT AVG(fare)
FROM passengers
WHERE pclass = 1) AS Fare_First_class,
            
(SELECT AVG(fare)
FROM passengers
WHERE pclass = 2) AS Fare_Second_class,
            
(SELECT AVG(fare)
FROM passengers
WHERE pclass = 3) AS Fare_Third_class;
'''

q7 = 'How many siblings/spouses aboard on average, by passenger class? By survival?'
Q7 = '''
SELECT  
(SELECT AVG(siblings_spouses_aboard)
FROM passengers
WHERE pclass = 1) AS Siblings_First_class,
            
(SELECT AVG(siblings_spouses_aboard)
FROM passengers
WHERE pclass = 2) AS Siblings_Second_class,

(SELECT AVG(siblings_spouses_aboard)
FROM passengers
WHERE pclass = 3) AS Siblings_Third_class,

(SELECT AVG(siblings_spouses_aboard)
FROM passengers
WHERE survived = 0) AS Siblings_fatalities,

(SELECT AVG(siblings_spouses_aboard)
FROM passengers
WHERE survived = 1) AS Siblings_survivors;
'''

q8 = 'How many parents/children aboard on average, by passenger class? By survival?'
Q8 = '''
SELECT  
(SELECT AVG(parents_children_aboard)
FROM passengers
WHERE pclass = 1) AS Parents_First_class,

(SELECT AVG(parents_children_aboard)
FROM passengers
WHERE pclass = 2) AS Parents_Second_class,

(SELECT AVG(parents_children_aboard)
FROM passengers
WHERE pclass = 3) AS Parents_Third_class,

(SELECT AVG(parents_children_aboard)
FROM passengers
WHERE survived = 0) AS Parents_fatalities,

(SELECT AVG(parents_children_aboard)
FROM passengers
WHERE survived = 1) AS Parents_survivors;
'''

q9 = 'Do any passengers have the same name?'
Q9 = '''
SELECT name, id, COUNT(*)
FROM passengers
GROUP BY name, id
HAVING COUNT(*) > 1
'''


q10 = '''(Bonus! Hard, may require pulling and processing with Python) How many married
  couples were aboard the Titanic? Assume that two people (one `Mr.` and one
  `Mrs.`) with the same last name and with at least 1 sibling/spouse aboard are
  a married couple.'''
  

questions= [q1,q2,q3,q4,q5,q6,q7,q8,q9]
queries = [Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9]



for i in range(0,9):
    cursor.execute(queries[i])
    result = cursor.fetchall()
    print(questions[i])
    print("RESULT:", type(result))
    print(result)
    print('---------------')

print(q10)
df = pd.read_csv(CSV_FILEPATH)

col = []
for i in range(0,len(df)):
    words = df['Name'][i].split()
    col.append(words[-1])
col2 = []
for i in range(0,len(df)):
    words = df['Name'][i].split()
    col2.append(words[0])

df['last_name'] = col
df['prefix'] = col2

mr = df[df['prefix']== 'Mr.']
mrs = df[df['prefix']== 'Mrs.']

lnames = mr['last_name'].to_list()
lnames_mrs = mrs['last_name'].to_list()

col3 = []
for i in range(0,len(lnames)):
  if lnames[i] in lnames_mrs:
    col3.append(lnames[i])

print(len(col3))






