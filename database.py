import sqlite3
import os

DB_PATH = "data/tasks.db"

def connect():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            deadline TEXT,
            priority INTEGER,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()
