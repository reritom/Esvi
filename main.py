from esvi.database_handler import DatabaseHandler
from test_models.contact import Contact
from test_models.message import Message
import os, time

if __name__=='__main__':
    '''
    esvi = DatabaseHandler()

    esvi.create_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.esvi'))

    esvi.create_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'new.esvi'))

    print("Locking db")

    esvi._lock()
    time.sleep(5)
    print("Unlocking db")
    esvi._unlock()
    '''
    contact = Contact(age=15, name="Tom")
    contact.get_fields()
    contact.get_json()

    contact.set('age', 20)
    contact.get_json()
    print(contact._staged_changes)
    contact.save()

    message = Message()
