import os

class Database():
    database_header_definition = b'<Database>'
    database_tail_definition = b'</Database>'
    models_header_definiton = b'<Models>'
    models_tail_definition = b'</Models>'
    size_header_element = b'<size>'
    size_tail_element = b'</size>'

    def __init__(self, path):
        self.path = path
        self._validate_db_header()
        self._validate_db_tail()
        self._validate_models_header()
        self.cursor = 0

    def _validate_db_header(self):
        with open(self.path, 'rb') as f:
            header = f.read(len(Database.database_header_definition))
            print(header)
            self.cursor = f.tell()

        if not Database.database_header_definition == header:
            raise Exception("Invalid DB header")

    def _validate_models_header(self):
        cursor = len(Database.database_header_definition)
        with open(self.path, 'rb') as f:
            f.seek(cursor)
            content_header = f.read(len(Database.models_header_definiton))
            print(content_header)
            self.cursor = f.tell()

    def _validate_db_tail(self):
        with open(self.path, 'rb') as f:
            f.seek(-len(Database.database_tail_definition), os.SEEK_END) # Offset from file, and start at end of file
            tail = f.read(len(Database.database_tail_definition))
            print(tail)

        if not Database.database_tail_definition == tail:
            raise Exception("Invalid DB tail")

    def insert_model_definition(self, definition):
        pass

    def get_model_definitions(self):
        pass

    def get_model_definition(self, model_name):
        pass

    def remove_model_definition(self, model_name):
        pass

    def insert_model(self, model):
        pass

    def remove_model(self, model_pk):
        pass

    def _check_model_fits_definition(self):
        pass
