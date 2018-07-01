from esvi.database_handler import DatabaseHandler
from test.test_models.contact import Contact
from test.test_models.message import Message
import os, time



if __name__=='__main__':

    handler = DatabaseHandler()
    handler.create_db(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.esvi'))
    handler.set_global_connection()


    print("Initial object is")
    print(Contact)


    Contact.get_fields()
    print("New object is {}".format(Contact))

    contact = Contact.create(age=15, name="Tom")
    print("Contact object is {}".format(contact))


    Message.get_fields()
    Contact.get_fields()
