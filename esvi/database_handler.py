from esvi.connection import Connection
import os, json, uuid, datetime, time

class DatabaseHandler():

    def __init__(self):
        """
        We will search for any db at this level, else we'll set a flag requiring a manual setup
        """

        self.this_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = self._discover_in_dir(self.this_dir)

    def _discover_in_dir(self, dir_path):
        """
        Search this dir for any esvi dbs
        """
        for this_file in os.listdir(dir_path):
            if this_file.endswith('.esvi'):
                return os.path.join(dir_path, this_file)

        return None

    def set_global_connection(self):
        global esvi_cnx
        esvi_cnx = self.get_connection()
        print(globals())

    def create_db(self, path):
        """
        Check if the db already exists
        Initialise an empty db
        """
        if os.path.isfile(path):
            self.db_path = path
            print("DB already exists")
            return

        print(path)

        self.db_path = path

        print("Opening the base db")
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'basedb.xml'), 'r') as f:
            base = f.read()
            print("Reading the base as {0}".format(base))

    def get_connection(self):
        if not self.db_path:
            raise Exception("No DB path")

        return Connection(self.db_path)

    def retrieve_models(self):
        pass

    def add_model(self):
        pass

    def delete_model(self):
        pass


    @staticmethod
    def check_integrity(db_path):
        pass
