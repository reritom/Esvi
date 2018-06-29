from esvi.database_handler import DatabaseHandler
from esvi.access_setup import setup_database
from test_models.contact import Contact
from test_models.message import Message
import os, time


global esvi_cnx

if __name__=='__main__':
    esvi_cnx = setup_database()

    print(globals())
    contact = Contact()

    contact = contact.handler.create(age=15, name="Tom")

    '''
    contact.get_json()

    contact.set('age', 20)
    contact.get_json()
    print(contact._staged_changes)
    contact.save()
    '''
