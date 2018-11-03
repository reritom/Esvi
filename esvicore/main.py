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

    client_instance_2 = {'business': 2,
                       'name': "Burger King",
                       'description': "A burger company"}

    db.insert_model(model_name="Client", model_instance=client_instance)
    db.insert_model(model_name="Client", model_instance=client_instance_2)

    person_instance = {'age': 12,
                       'name': "Rob"}
    db.insert_model(model_name="Person", model_instance=person_instance)

    definition = {'model_name': 'Plant',
                  'fields': {'type': {'type': str, 'pk': True}}}

    db.add_model_definition(definition)
    db.insert_model(model_name="Plant", model_instance={'type': 'tree'})

    print(db.get_all_given_models(model_name="Client"))