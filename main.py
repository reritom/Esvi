from esvi import Esvi
import os, time

if __name__=='__main__':
    cnx = Esvi()
    print("DB located at {0}".format(cnx.db_path))

    cnx.create_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.esvi'))

    cnx.create_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'new.esvi'))

    print("Locking db")

    cnx._lock()
    time.sleep(5)
    print("Unlocking db")
    cnx._unlock()
