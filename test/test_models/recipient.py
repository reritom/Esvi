from esvi import model
from esvi import fields
from test.test_models.contact import Contact
from test.test_models.message import Message

class Recipient(model.Model):
    recipient_id = fields.StringField(primary=True)
    contact = fields.ForeignKey(Contact)
    message = fields.ForeignKey(Message)
