from test.test_models.contact import Contact
from test.test_models.message import Message
from esvi.esvi_setup import EsviSetup
import os, time



if __name__=='__main__':

    setup = EsviSetup()
    setup.set_database_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.sqlite'))
    setup.set_global_connection()

    #Contact._initialise_in_db()


    print("Initial object is")
    print(Contact)

    Contact._get_defition_from_db()


    Contact.get_fields()
    print("New object is {}".format(Contact))

    contact = Contact.create(age=15, name="Tom", contact_id="6xx")
    contact = Contact.retrieve("6xx")
    print("Contact object is {}".format(contact))



    Message.get_fields()
    Contact.get_fields()
