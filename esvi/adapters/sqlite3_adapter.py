import sqlite3

class Sqlite3Adapter():
    def __init__(self, cnx):
        self.cnx = cnx
        self.db = sqlite3.connect(cnx.get_path())

    def create_model(self, query):
        pass

    def create(self, query):
        with sqlite3.connect(cnx.get_path()) as conn:
            pass
        if conn:
            conn.close

    def retrieve(self, query):
        with sqlite3.connect(cnx.get_path()) as conn:
            pass
        if conn:
            conn.close

    def update(self, query):
        def retrieve(self, query):
            with sqlite3.connect(cnx.get_path()) as conn:
                pass
            if conn:
                conn.close

    def filter(self, query):
        def retrieve(self, query):
            with sqlite3.connect(cnx.get_path()) as conn:
                pass
            if conn:
                conn.close

    def get_models(self):
        with sqlite3.connect(cnx.get_path()) as conn:
            conn.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = conn.cursor.fetchall()
        if conn:
            conn.close

        return models
