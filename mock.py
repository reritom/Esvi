# This file is for mocking how I'd like to interact with Esvi

# I'll need to run a setup file which will create each model in the db (migrate.py)
# This will search for models and create them in the db

from models.contact import Contact

# Create a contact
contact = Contact.create(name='Jack',
                           message=Message.retrieve(message_id='yyy-yyy-yyy'),
                           contact_id="xxx-xxx-xxx")

# Retrieve all
contacts = Contact.retrieve_all()

# Retrieve one using the primary key
contact = Contact.retrieve(contact_id="xxx-xxx-xxx")

# Retrieve all for given criteria
contact = Contact.filter(age_between_inc=(20,30), height_less_or_equal=40, weight=greaterthan(60))
