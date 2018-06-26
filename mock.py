# This file is for mocking how I'd like to interact with Esvi

# I'll need to run a setup file which will create each model in the db (migrate.py)
# This will search for models and create them in the db

from models.contact import Contact

# Create a contact
contact = Contact.models.create(name='Jack',
                                message=message.models.retrieve(message_id='yyy-yyy-yyy'),
                                contact_id="xxx-xxx-xxx")

# Retrieve all
contacts = Contact.models.retrieve_all()

# Retrieve one using the primary key
contact = Contact.models.retrieve(contact_id="xxx-xxx-xxx")

# Retrieve all for given criteria
contact = Contact.models.filter(age=lessthan(20), height=equalto(40), weight=greaterthan(60))
