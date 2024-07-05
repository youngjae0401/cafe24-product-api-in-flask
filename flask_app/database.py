from flask import g
from mysql.connector import connect, Error
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.db_config = DB_CONFIG

    def get_connection(self):
        if 'db_conn' not in g:
            try:
                g.db_conn = connect(**self.db_config)
            except Error as e:
                raise
        return g.db_conn

    def close_connection(self):
        db_conn = g.pop('db_conn', None)
        if db_conn is not None:
            db_conn.close()
