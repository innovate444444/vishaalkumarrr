import sqlite3

# Connect to SQLite database (or you can use other DBMS)
conn = sqlite3.connect('login_database.db')
cursor = conn.cursor()

# Create a table for users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT CHECK(user_type IN ('engineer', 'operator', 'developer')) NOT NULL
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()
