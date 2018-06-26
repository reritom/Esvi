from models import EsviModel

class Contact(EsviModel):
    name = "Contact"

    #fields = [Esvi.Field('name'),
    #          Esvi.PrimaryKey('contact_id'),
    #          Esvi.ForeignKey('message_id')]
