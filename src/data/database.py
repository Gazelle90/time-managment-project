import psycopg2
from src.data.config import get_database_credentials


def get_connection():
    host, database, user, password, port = get_database_credentials()

    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )

