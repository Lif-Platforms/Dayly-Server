import uuid
import sqlite3

database_path = None

# Allows database path to be set by main script
def set_db_path(path):
    global database_path
    database_path = path

def new_post(title, description, author, content,):
    # Generate a random UUID
    post_id = str(uuid.uuid4())

    # Connects to database
    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # Adds post to database
    c.execute("INSERT INTO posts (id, author, title, description, content) VALUES (?, ?, ?, ?, ?)", (post_id, author, title, description, content))
    conn.commit()

    conn.close()