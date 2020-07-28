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

cursor.execute(
    '''
    CREATE TABLE passengers ( 
        id  SERIAL PRIMARY KEY, 
        survived   int,
        pclass    int,
        name  varchar(100),
        sex   varchar(40),
        age   int,
        siblings_spouses_aboard   int,
        parents_children_aboard  int,
        fare  float);
    '''
)


df = pd.read_csv(CSV_FILEPATH)

for i in range(0,len(df)):
    survived = df['Survived'][i]
    pclass = df['Pclass'][i]
    name = df['Name'][i].replace("'"," ")
    sex = df['Sex'][i]
    age = df['Age'][i]
    siblings = df['Siblings/Spouses Aboard'][i]
    parents = df['Parents/Children Aboard'][i]
    fare = df['Fare'][i]

    cursor.execute(
        f'''
        INSERT INTO passengers (survived, pclass, name, sex, age, siblings_spouses_aboard, 
        parents_children_aboard, fare) VALUES(
            {survived},
            {pclass},
            '{name}',
            '{sex}',
            {age},
            {siblings},
            {parents},
            {fare})
        '''
    )

connection.commit() 

q1 = 'How many fatalilties'
cursor.execute(
    '''
    SELECT COUNT(*) as FATALITIES
    FROM passengers
    WHERE survived = 0
    ''')

result = cursor.fetchall()
print(q1)
print("RESULT:", type(result))
print(result)
print('---------------')

q2 = 'How many people had family aboard'

cursor.execute(
    '''
    SELECT COUNT(*) as Families
    FROM passengers
    WHERE siblings_spouses_aboard > 0 or parents_children_aboard > 0
    ''')

result = cursor.fetchall()
print(q2)
print("RESULT:", type(result))
print(result)
print('---------------')

q3 =  'Whats the Average Price of fare'

cursor.execute(
    '''
    SELECT AVG("fare") as average_fare
    FROM passengers
   
    ''')

result = cursor.fetchall()
print(q3)
print("RESULT:", type(result))
print(result)
print('---------------')