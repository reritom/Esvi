from esvi import fields

class EsviModel():

    def __init__(self, **kwargs):
        # Initialise the model name
        self.name = getattr(self.__class__, 'model_name') if hasattr(self.__class__, 'model_name') else self.__class__.__name__ + "Model"

        # Initialise the fields
        self.fields = dict()

        # Primary Key flag
        pk_flag = False

        # Here we grab any fields from the child class attributes
        for value in dir(self.__class__):
            class_attribute = getattr(self.__class__, value)
            if hasattr(class_attribute, '__class__') and class_attribute.__class__.__base__ == fields.BaseField:
                self.fields[value] = class_attribute
                if class_attribute.__class__ == fields.PrimaryKey:
                    pk_flag = True

        if not pk_flag:
            raise Exception("Model {0} is missing a primary key field".format(self.name))

        # Initialise the content
        self.content = dict()

        # Here we validate that the model is being initialised with enough information
        for field_name, definition in self.fields.items():
            # Check if it is in the kwargs
            if field_name in kwargs:
                # TODO validate that the kwarg is correct type for the field
                definition.validate(kwargs[field_name])
                self.content[field_name] = kwargs[field_name]

            # Check if it has a default value
            elif definition.has_default():
                self.content[field_name] = definition.get_default()

            else:
                raise Exception(field_name + " missing as parameter and has no default")

        # Any updates to the fields are stored here before being saved
        self._staged_changes = set()

    def get_json(self):
        print(self.content)

    def get_fields(self):
        print(self.fields)

    def set(self, field, value):
        if field not in self.fields:
            raise Exception("Attempting to set invalid field {0} for model {1}".format(field, self.name))

        self.fields[field].validate(value)
        self.content[field] = value
        self._staged_changes.add(field)


    def get(self, field):
        if field not in self.fields:
            raise Exception("Attempting to get invalid field {0} for model {1}".format(field, self.name))

        return self.content[field]

    def save(self):
        print("Saving the {0}, there are changes to fields {1}".format(self.name, self._staged_changes))

    @staticmethod
    def create():
        pass

    @staticmethod
    def retrieve_all():
        pass

    @staticmethod
    def retrieve():
        pass

    @staticmethod
    def filter():
        pass
