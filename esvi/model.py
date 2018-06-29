from esvi import fields
from esvi.model_handler import ModelHandler

class Model():

    def __init__(self):
        # Initialise the model name
        self.name = getattr(self.__class__, 'model_name') if hasattr(self.__class__, 'model_name') else self.__class__.__name__ + "Model"

        # Initialise the fields
        self.fields = dict()

        # Primary Key flag
        # # TODO: Fix multi PK bug
        pk_flag = 0

        # Here we grab any fields from the child class attributes
        for value in dir(self.__class__):
            class_attribute = getattr(self.__class__, value)
            if hasattr(class_attribute, '__class__') and class_attribute.__class__.__base__ == fields.BaseField:
                self.fields[value] = class_attribute
                if class_attribute.__class__ == fields.PrimaryKey:
                    pk_flag += 1

        if pk_flag is not 1:
            raise Exception("Model {0} is missing a primary key field".format(self.name))


        self.handler = ModelHandler(model_name=self.name, model_fields=self.fields)

    def get_fields(self):
        print(self.fields)
