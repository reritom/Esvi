import datetime
from esvi import fields
from esvi import exceptions

class BaseField():
    def __init__(self, default=None, primary=False):
        self.default = default
        self.primary = primary
        self.foreign = False

    def has_default(self) -> bool:
        return True if self.default is not None else False

    def get_default(self):
        return self.default

    def is_primary(self) -> bool:
        return self.primary

    def get_type(self) -> str:
        print("Type is {}".format(self.__class__.__name__))
        return self.__class__.__name__

    def is_foreign(self) -> bool:
        return self.foreign

class ForeignKey(BaseField):
    def __init__(self, reference):
        super().__init__()
        self.foreign = True
        self.reference = reference

        # Lets just check that the reference is a valid model
        from esvi.model import Model

        if not reference.__base__ == Model:
            raise exceptions.InvalidForeignKeyDefinition()

    def get_reference(self):
        return self.reference

    def validate(self, value):
        # TODO here we will validate that the value is that of an EsviModel class
        if not value._model_name == self.reference.model_name:
            raise exceptions.FieldValidationException("Reference model name doesn't not match instance")



class StringField(BaseField):
    field_type = str

    def __init__(self, default=None, primary=False):
        super().__init__(default, primary)

    def validate(self, value: str) -> bool:
        print("Validating stringfield, value is {0}, type is {1}, expected type is {2}".format(value, type(value), self.field_type))
        #return True if type(value) is StringField.field_type else False
        if not type(value) is self.field_type:
            raise exceptions.FieldValidationException("Value {0} is type {1} but should be type {2}".format(value, type(value), self.field_type))

class JSONField(BaseField):
    field_type = dict

    def __init__(self, default=None, primary=False):
        if primary:
            raise exceptions.UnsupportedFieldForPrimaryKey()

        super().__init__(default, primary)

    def validate(self, value):
        if not type(value) is JSONField.field_type:
            raise exceptions.FieldValidationException("Value {0} is type {1} but should be type {2}".format(value, type(value), self.field_type))

class ObjectField(BaseField):
    field_type = object

    def __init__(self, reference, default=None, primary=False):
        if primary:
            raise exceptions.UnsupportedFieldForPrimaryKey()

        if not (hasattr(reference, 'serialise') and hasattr(reference, 'deserialise')):
            raise exceptions.InvalidObjectFieldException("Object field object requires serialise and deserialise methods")

        super().__init__(default, primary)
        self.reference = reference

    def validate(self, value):
        if not (hasattr(value, 'serialise') and hasattr(value, 'deserialise')):
            raise exceptions.FieldValidationException("Value {0} is type {1} but should be type {2}".format(value, type(value), self.field_type))

class IntegerField(BaseField):
    field_type = int

    def __init__(self, default=None, primary=False):
        super().__init__(default, primary)

    def validate(self, value: int) -> bool:
        print("Validating IntegerField, value is {0}, type is {1}, expected type is {2}".format(value, type(value), self.field_type))
        #return True if type(value) is StringField.field_type else False
        if not type(value) is self.field_type:
            raise exceptions.FieldValidationException("Value {0} is type {1} but should be type {2}".format(value, type(value), self.field_type))

class DateTimeField(BaseField):
    field_type = datetime.datetime

    def __init__(self, default=None, primary=False):
        if primary:
            raise exceptions.UnsupportedFieldForPrimaryKey()

        super().__init__(default, primary)

    def validate(self, value: datetime) -> bool:
        if not isinstance(value, field_type):
            raise exceptions.FieldValidationException("Value {0} is type {1} but should be type {2}".format(value, type(value), self.field_type))
