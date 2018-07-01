import os

from esvi.database_handler import DatabaseHandler

def test_create_db():
    handler = DatabaseHandler()
    handler.create_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.esvi'))
    handler.format_db()
    handler.read_formatted()

    handler.print_db()
