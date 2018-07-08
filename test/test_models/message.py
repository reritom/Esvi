from esvi import model
from esvi import fields

class Message(model.Model):

    message_id = fields.StringField(default=20, primary=True)
