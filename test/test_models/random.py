from esvi import model
from esvi import fields

try:
    from test_objects.car import Car
except:
    from test.test_models.test_objects.car import Car

class RandomModel(model.Model):

    time = fields.DateTimeField()
    id_field = fields.StringField(primary=True)
    number = fields.IntegerField(default=0)
    obj = fields.ObjectField(Car)
    json_field = fields.JSONField()