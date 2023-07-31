import psycopg2 as pg
from json import load
import os

directory = os.path.dirname(os.path.relpath(__file__))

def config(credentials_file=os.path.join(directory, 'credentials.json')):
    """Database connection credentials.

    Args:
        credentials_file (str, optional): Path to the credentials file. './credentials.json'.

    Raises:
        ValueError: Path to an existing credentials file need to be specified.

    Returns:
        pg.connect object: Psycopg2 valid connection object.
    """
    if os.path.exists(credentials_file):
        content = load(open(credentials_file))
        host, database = content['host'], content['database']
        user, password = content['user'], content['password']
        conn = pg.connect(host=host, database=database,
                          user=user, password=password)
        return conn
    
    else:
        raise ValueError("Make sure that the credentials file exists.")