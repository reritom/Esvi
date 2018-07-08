from esvi import model
from esvi import fields

class Contact(model.Model):
    model_name = "Contact"

    contact_id = fields.StringField(primary=True)
    name = fields.StringField()
    age = fields.IntegerField(default=0)
    #message = fields.ForeignKey(default='EmptyMessage')
