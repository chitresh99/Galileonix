import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    DB_STRING=os.getenv("DB_STRING")
    conn=psycopg2.connect(DB_STRING)
    print("Connection to PostgreSQL successful!")

    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        );
    """)
    conn.commit() # Commit changes to the database
    print("Table 'users' created (if it didn't exist).")

    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", ("Alice", "alice@example.com"))
    conn.commit()
    print("Data inserted into 'users' table.")
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")