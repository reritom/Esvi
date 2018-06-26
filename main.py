from esvi import Esvi
from test_models.contact import Contact
import os, time

if __name__=='__main__':
    '''
    esvi = Esvi()
    print("DB located at {0}".format(cnx.db_path))

    esvi.create_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.esvi'))

    esvi.create_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'new.esvi'))

    print("Locking db")

    esvi._lock()
    time.sleep(5)
    print("Unlocking db")
    esvi._unlock()
    '''
    contact = Contact()

    print(contact)
