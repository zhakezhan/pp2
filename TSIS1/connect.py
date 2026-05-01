import psycopg2
from psycopg2 import OperationalError
from config import load_config


def connect():
    try:
        config = load_config()
        connection = psycopg2.connect(**config)
        return connection
    except OperationalError as e:
        print("Connection error:", e)
        return None