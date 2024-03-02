import os
import pandas as pd
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# pd.read_csv(filename).to_sql(tablename, con)

if __name__ == '__main__':
    main()

    database = r"db.sqlite3"

    # create a database connection
    conn = create_connection(database)