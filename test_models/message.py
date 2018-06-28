from esvi import models
from esvi import fields

class Message(models.EsviModel):

    message_id = fields.PrimaryKey(default=20)
