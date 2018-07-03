from esvi.connection import Connection
import os, json, uuid, datetime, time
from lxml import etree

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

    def format_db(self):
        """
        This is for formatting the mocked XML db so it doesn't have whitespace between elements
        """
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'basedb.xml'), 'r') as f:
            base = f.read()

        parser = etree.XMLParser(remove_blank_text=True)
        elem = etree.XML(base, parser=parser)
        print(etree.tostring(elem))

        with open(os.path.join(self.this_dir, 'formatted.xml'), 'wb') as f:
            f.write(etree.tostring(elem))

    def get_formatted_path(self):
        return os.path.join(self.this_dir, 'formatted.xml')

    def read_formatted(self):
        with open(os.path.join(self.this_dir, 'formatted.xml'), 'rb') as f:
            for i in range(10):
                c = f.read(1)
                print('value {}, Position {}'.format(c, f.tell()))
                f.seek(f.tell() + 1)

    def get_connection(self):
        if not self.db_path:
            raise Exception("No DB path")

        return Connection(self.db_path)

    @staticmethod
    def check_integrity(db_path):
        pass
