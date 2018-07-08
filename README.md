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
  first_name = fields.StringField()
  surname = fields.StringField()
  age = fields.IntegerField()
  email_address = fields.StringField(default=None) # There is also support for default values
```

### Interacting with your model
Before interacting with your model, you need to set up your database connection. For simplicitly, at the beginning of your flow, you will need to do the following:
```

from esvi.esvi_setup import EsviSetup

setup = EsviSetup()
setup.set_database_path(<i>path_to_your_db</i>)
setup.set_global_connection() # This creates a connection object accessible throughout the model interface, this is required
```

Now, from inside your flow you can do the following:
- Create a new instance of your model
```
contact = Contact.create(first_name="Tony", surname="Stark", age=43)
```
This returns a ModelInstance object which has its own set of interactions.
The ModelInstance uses getters and setters to change its value, and then has an explicit save function for commiting the changes to the database
```
contact.set("age", 44)
contact.save()
```
If you are done with a ModelInstance, you can delete it from the database using delete().
```
contact.delete()
```
If you attempt anything with this object now, you'll raise an InstanceDeletedException.



## Things to be implemented
- Foreign Key support
- Datetime field support
