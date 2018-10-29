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
    definition = {'model_name': 'Person',
                  'fields': {'age': {'type': int, 'pk': True, 'default': 0},
                             'name': {'type': str}}}

    db.add_model_definition(definition)

    definition = {'model_name': 'Client',
                  'fields': {'business': {'type': int, 'pk': True},
                             'name': {'type': str},
                             'description': {'type': str}}}

    db.add_model_definition(definition)

    db.get_model_definition("Client")

    client_instance = {'business': 1,
                       'name': "Jacks patch",
                       'description': "A gardening company"}

    db.insert_model(model_name="Client", model_instance=client_instance)
