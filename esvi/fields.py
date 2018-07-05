class BaseField():
    def __init__(self, **kwargs):
        self.default = kwargs['default'] if kwargs.get('default', False) else None
        self.primary = False

    def has_default(self):
        return True if self.default is not None else False

    def get_default(self):
        return self.default

    def get_type(self):
        return self.type

    def is_primary(self):
        return self.primary

class PrimaryKey(BaseField):
    type = 'TEXT'

    def validate(self, value):
        return True

    def is_primary(self):
        return True

class ForeignKey(BaseField):
    def validate(self, value):
        # TODO here we will validate that the value is that of an EsviModel class
        return True

class StringField(BaseField):
    type = 'TEXT'
    field_type = str

    def validate(self, value):
        print("Validating stringfield, value is {0}, type is {1}, expected type is {2}".format(value, type(value), StringField.field_type))
        #return True if type(value) is StringField.field_type else False
        if not type(value) is StringField.field_type:
            raise Exception("Value {0} is type {1} but should be type {2}".format(value, type(value), StringField.field_type))

class IntegerField(BaseField):
    type = 'INTEGER'
    field_type = int

    def validate(self, value):
        print("Validating IntegerField, value is {0}, type is {1}, expected type is {2}".format(value, type(value), IntegerField.field_type))
        #return True if type(value) is StringField.field_type else False
        if not type(value) is IntegerField.field_type:
            raise Exception("Value {0} is type {1} but should be type {2}".format(value, type(value), IntegerField.field_type))

class DateTimeField(BaseField):
    def validate(self, value):
        return True
