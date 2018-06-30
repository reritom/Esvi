from esvi.database_handler import DatabaseHandler
from esvi.access_setup import setup_database
from test.test_models.contact import Contact
from test.test_models.message import Message
import os, time



if __name__=='__main__':
    connection = setup_database()


    print("Initial object is")
    print(Contact)


    Contact.get_fields()
    print("New object is {}".format(Contact))

    contact = Contact.create(age=15, name="Tom")
    print("Contact object is {}".format(contact))


    Message.get_fields()
    Contact.get_fields()
