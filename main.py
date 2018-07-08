from test.test_models.contact import Contact
from test.test_models.message import Message
from esvi.esvi_setup import EsviSetup
import os, time, uuid



if __name__=='__main__':

    setup = EsviSetup()
    setup.set_database_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.sqlite3'))
    setup.set_global_connection()

    Contact._initialise_in_db()


    print("Initial object is")
    print(Contact)

    Contact._get_defition_from_db()


    Contact.get_fields()
    print("New object is {}".format(Contact))

    Contact.retrieve_all()

    pk = str(uuid.uuid4())[:5]
    print("PK is {}".format(pk))
    contact = Contact.create(age=15, name="Tom", contact_id=pk)
    contact = Contact.retrieve(pk)
    print("Contact object is {}".format(contact))

    print("Lets try and iterate over it")
    for key in contact:
        print(key)

    print("Lets try and delete this new contact")
    contact.delete()
    print("Contact deleted is {}".format(contact))
    print("Try and retrieve after deletion")
    contact = Contact.retrieve(pk)
    print("Contact is {}".format(contact))

    """

    contact.set("age", 30)
    contact.save()
    contacts = Contact.retrieve_all()
    print("Lets iterate")
    for contact in contacts:
        contact.pretty()

    print("Lets check the existance")
    if Contact.retrieve_all().exists():
        print("Yay it exists")



    Message.get_fields()
    Contact.get_fields()
    """
