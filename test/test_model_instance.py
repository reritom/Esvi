from esvi.model_instance import ModelInstance
from esvi import fields

def test_model_instance():
    model_name = 'contact'
    model_fields = {'age': fields.IntegerField(),
                    'name': fields.StringField()}
    model_content = {'age':5, 'name':"Jack"}

    contact = ModelInstance(model_name, model_fields, model_content)
    print(contact)
