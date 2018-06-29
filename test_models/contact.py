from esvi import model
from esvi import fields

class Contact(model.Model):
    model_name = "Contact"

    contact_id = fields.PrimaryKey(default="0")
    name = fields.StringField()
    age = fields.IntegerField()
    message = fields.ForeignKey(default='EmptyMessage')
