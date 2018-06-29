from esvi import model
from esvi import fields

class Message(model.Model):

    message_id = fields.PrimaryKey(default=20)
