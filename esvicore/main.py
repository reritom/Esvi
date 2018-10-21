from database import Database

if __name__=='__main__':
    '''
    with open("formatted_backup.xml", "rb") as f:
        backup = f.read()

    with open("formatted.xml", "wb") as f:
        f.write(backup)

    db = Database("formatted.xml")
    '''

    db = Database.initialise_empty_db('new.esvi')
