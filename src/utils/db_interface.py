import uuid
import sqlite3

def new_post(title, description, author, content,):
    # Generate a random UUID
    post_id = str(uuid.uuid4())

    # Connects to database
    conn = sqlite3.connect("database/database.db")
    c = conn.cursor()

    # Adds post to database
    c.execute("INSERT INTO posts (id, author, title, description, content) VALUES (?, ?, ?, ?, ?)", (post_id, author, title, description, content))
    conn.commit()

    conn.close()