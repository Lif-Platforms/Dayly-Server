import uuid
import mysql.connector
from mysql.connector.constants import ClientFlag

# Allows database path to be set by main script
def set_db_config(config):
    global db_config
    db_config = config

def connect_to_database():
    # Handle connecting to the database
    def connect():
        global conn

        # Define configurations
        mysql_configs = {
            "host": db_config['mysql-host'],
            "port": db_config['mysql-port'],
            "user": db_config['mysql-user'],
            "password": db_config['mysql-password'],
            "database": db_config['mysql-database'], 
        }

        # Check if SSL is enabled
        if db_config['mysql-ssl']:
            # Add ssl configurations to connection
            mysql_configs['client_flags'] = [ClientFlag.SSL]
            mysql_configs['ssl_ca'] = db_config['mysql-cert-path']

        conn = mysql.connector.connect(**mysql_configs)
    
    # Check if there is a MySQL connection
    if conn is None:
        connect()
    else:
        # Check if existing connection is still alive
        if not conn.is_connected():
            connect()

def new_post(title, description, author, content,):
    connect_to_database()

    # Generate a random UUID
    post_id = str(uuid.uuid4())

    cursor = conn.cursor()

    # Adds post to database
    cursor.execute("INSERT INTO posts (post_id, author, title, description, uploads, creation_date) VALUES (%s, %s, %s, %s, %s)", (post_id, author, title, description, content, None))
    conn.commit()

    conn.close()