import sqlite3

connection = sqlite3.connect("resume.db", check_same_thread=False)
cursor = connection.cursor()


def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT
        )
    """)

    connection.commit()


def save_chat(role, content):
    cursor.execute("""
        INSERT INTO chat_history (role, content)
        VALUES (?, ?)
    """, (role, content))
    connection.commit()

