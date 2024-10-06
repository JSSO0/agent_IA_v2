# db_config.py
import psycopg2

def create_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="agent_avant",
        user="postgres",
        password="1234"
    )
