from esvi import models
from esvi import fields

class Contact(models.EsviModel):
    model_name = "Contact"

    contact_id = fields.PrimaryKey(default="0")
    name = fields.StringField()
    age = fields.IntegerField()
    message = fields.ForeignKey(default='EmptyMessage')
