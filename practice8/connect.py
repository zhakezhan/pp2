import psycopg2
from config import load_config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = load_config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection Error: {error}")
        return None