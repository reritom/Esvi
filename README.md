# Esvi

Esvi is a model interface that for easily adding new databases. Currently it supports sqlite3 and esvicore.
The model interface creates a clear seperation between the database and your flow

## How does it work?
In your code you can define Models by inheriting from a Model. Inside your definition you set the field names for your model, and their types, such as text fields, datetime fields, integer fields, and foreign keys. You can also explicitly set the model name, or implicitly use the class name as the model name.

### A model example
```
from esvi import model
from esvi import fields

class Contact(model.Model):
  first_name = fields.StringField(primary=True)
  surname = fields.StringField()
  age = fields.IntegerField()
  email_address = fields.StringField(default=None)
```

### Interacting with your model
Before interacting with your model, you need to set up your database connection.
For simplicitly, at the beginning of your flow, you will need to do the following:
```

from esvi.esvi_setup import EsviSetup

setup = EsviSetup()
setup.set_database_path(path_to_your_db)

# This creates a connection object accessible throughout the model interface, this is required
setup.set_global_connection()
```

Now, from inside your flow you can do the following:
- Create a new instance of your model
```
contact = Contact.create(first_name="Tony", surname="Stark", age=43)
```
This returns a ModelInstance object which has its own set of interactions.
The ModelInstance uses getters and setters to change its value, and then has an explicit save function for committing the changes to the database
```
contact.set("age", 44)
contact.save()
```
If you are done with a ModelInstance, you can delete it from the database using delete().
```
contact.delete()
```
If you attempt anything with this object now, you'll raise an InstanceDeletedException.

- Retrieving your models
There are two ways to retrieve a model. You can either retrieve by primary key, or you can filter.
When you retrieve by primary key, you just need to pass the value of your primary key to the retrieve method
```
contact = Contact.retrieve(primary_key="Tom")
```
This returns the typical ModelInstance object.

However, if you wish to filter or retrieve all, then multiple models can be returned, and are therefore returned in a class called the ModelSet.
This is simply an iterable which contains a list of ModelInstances.
```
# This is a ModelSet
all_contacts = Contact.retrieve_all()

for contact in all_contacts:
  # contact is a ModelInstance
  print(contact.get('name'))
```
The ModelSet has the method <i>exists()</i> which returns a boolean for if the ModelSet contains any ModelInstances.
This can be used for validation.
```
if Contact.retrieve_all().exists():
  # Do something
else:
  # We have no contacts, do something else
```

## Things to be implemented
- Foreign Key support
- Datetime field support
- Esvicore adapter
- Specific Exceptions
