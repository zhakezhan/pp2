import psycopg2
from psycopg2 import OperationalError


def get_connection():

    try:
        connection = psycopg2.connect(
            host="localhost",
            database="phonebook",   
            user="postgres",           
            password="Urakbtu2025",
            port="2204"   
        )
        return connection
    except OperationalError as e:
        print(f"Error: {e}")
        return None