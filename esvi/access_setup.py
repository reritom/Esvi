# Here we need to check the DB with the db_handler, and then create a global connection, and search for models and check if they have been migrated

from esvi.database_handler import DatabaseHandler
import os

def setup_database():
    handler = DatabaseHandler()
    handler.create_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.esvi'))

    global esvi_cnx
    esvi_cnx = handler.get_connection()

    return esvi_cnx
