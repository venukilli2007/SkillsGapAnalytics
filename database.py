import sqlite3

conn = sqlite3.connect("skillsgap.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    college TEXT,
    course TEXT,
    career_goal TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    college TEXT,
    course TEXT,
    career_goal TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    skill TEXT NOT NULL,
    level TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database created successfully!")

conn.commit()
conn.close()

print("Database created successfully!")