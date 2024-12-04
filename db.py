import pandas as pd
import psycopg2

# Replace these with your connection details
conn_details = {
    "host": "localhost",
    "dbname": "cloud",
    "user": "postgres",
    "password": "manu123"
}

# Load data from Excel
data = pd.read_excel('papers.xlsx', engine='openpyxl')

# Find the maximum length of 'title' and 'author' strings
max_title_length = data['Title'].str.len().max()
max_author_length = data['Author'].str.len().max()

# Connect to PostgreSQL database
conn = psycopg2.connect(**conn_details)
cursor = conn.cursor()

# Create table if not exists (optional, run once)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS papers (
        id SERIAL PRIMARY KEY,
        title VARCHAR({}),
        author VARCHAR({}),
        url TEXT
    );
'''.format(int(max_title_length), int(max_author_length)))

conn.commit()

# Insert data into the database
for index, row in data.iterrows():
    cursor.execute(
        "INSERT INTO papers (title, author, url) VALUES (%s, %s, %s)",
        (row['Title'], row['Author'], row['URL'])
    )
    conn.commit()

cursor.close()
conn.close()
