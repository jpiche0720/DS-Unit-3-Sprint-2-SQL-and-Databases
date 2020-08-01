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
        prefix  varchar(20),
        last_name   varchar(100),
        sex   varchar(40),
        age   int,
        siblings_spouses_aboard   int,
        parents_children_aboard  int,
        fare  float);
    '''
)


df = pd.read_csv(CSV_FILEPATH)
words = df['Name'][0].split()
print(words[-1])

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

for i in range(0,len(df)):
    survived = df['Survived'][i]
    pclass = df['Pclass'][i]
    name = df['Name'][i].replace("'"," ")
    prefix = df['prefix'][i]
    last_name = df['last_name'][i].replace("'", " ")
    sex = df['Sex'][i]
    age = df['Age'][i]
    siblings = df['Siblings/Spouses Aboard'][i]
    parents = df['Parents/Children Aboard'][i]
    fare = df['Fare'][i]



    cursor.execute(
        f'''
        INSERT INTO passengers (survived, pclass, name, prefix, last_name, sex, age, siblings_spouses_aboard, 
        parents_children_aboard, fare) VALUES(
            {survived},
            {pclass},
            '{name}',
            '{prefix}',
            '{last_name}',
            '{sex}',
            {age},
            {siblings},
            {parents},
            {fare})
        '''
    )

connection.commit() 

