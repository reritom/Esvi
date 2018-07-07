import sqlite3, os

class Sqlite3Viewer():
    def __init__(self, db_path, cache=False):
        '''
            Initiate by creating an object for each table and creating the db connection
            :param db_path (string): Path to the DB
            :param cache (bool): For caching tables instead of making repeated db calls
        '''
        self.cache = cache
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.all_tables = {table[0]: None for table in self.get_all_tables()}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
        print("Exiting DBViewer")

    def get_all_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        print(tables)
        return tables

    def get_table(self, table_name):
        if table_name not in self.all_tables:
            raise Exception("Invalid table name")

        self.cursor.execute("SELECT * FROM {table};".format(table=table_name))
        rows = self.cursor.fetchall()

        self.get_table_columns(table_name)

    def get_table_columns(self, table_name):
        query = 'PRAGMA TABLE_INFO({})'.format(table_name)
        print("Getting colums for query {}".format(query))
        self.cursor.execute(query)
        #print(self.cursor.fetchall())
        columns = [tup[1] for tup in self.cursor.fetchall()]
        print(columns)

if __name__=='__main__':
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.sqlite3')
    print("Path is {}".format(db_path))
    with DBViewer(db_path, cache=True) as viewer:
        viewer.get_all_tables()
        viewer.get_table('Contact')
