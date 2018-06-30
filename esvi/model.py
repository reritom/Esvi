from esvi import fields
from esvi.query import Query
from esvi.model_instance import ModelInstance
from esvi.query_executor import QueryExecutor

class Model():
    child_retrieved = False

    def __new__(cls):
        # To allow the classmethods to access child properties without an explicit instanciation, this method gets called by each
        # classmethod. The following flag checks whether it has already been ran or not
        if cls.child_retrieved == True:
            return

        print("In model new")
        # Initialise the model name
        cls.model_name = getattr(cls, 'model_name') if hasattr(cls, 'model_name') else cls.__name__ + "Model"

        # Initialise the fields
        cls.model_fields = dict()

        # Primary Key flag
        pk_flag = 0

        # Here we grab any fields from the child class attributes
        for value in dir(cls):
            class_attribute = getattr(cls, value)
            if hasattr(class_attribute, '__class__') and class_attribute.__class__.__base__ == fields.BaseField:
                cls.model_fields[value] = class_attribute
                if class_attribute.__class__ == fields.PrimaryKey:
                    pk_flag += 1

        if pk_flag is not 1:
            raise Exception("Model {0} is missing a primary key field".format(cls.model_name))

        cls.child_retrieved = True
        return cls


    @classmethod
    def get_fields(cls):
        Model.__new__(cls)
        print(cls.model_fields)
        return cls.model_fields

    @classmethod
    def create(cls, **kwargs):
        Model.__new__(cls)

        # Initialise the content of this model
        content = dict()

        # Here we validate that the model is being initialised with enough information
        for field_name, definition in cls.model_fields.items():
            if field_name in kwargs:
                # Check if it is in the kwargs
                definition.validate(kwargs[field_name])
                content[field_name] = kwargs[field_name]
            elif definition.has_default():
                # Check if it has a default value
                content[field_name] = definition.get_default()
            else:
                raise Exception("{} missing as parameter and has no default".format(field_name))

        # Here we create the query and pass it to the executor
        query = Query(model_name=cls.model_name, action="create", content=content)
        executor = QueryExecutor()
        response = executor.execute(query)
        return ModelInstance(model_name=cls.model_name, model_content=response) if response else None

    @classmethod
    def retrieve(cls, primary_key_value):
        Model.__new__(cls)
        query = Query(model_name=cls.model_name, action="retrieve", content=primary_key_value)
        executor = QueryExecutor()
        response = executor.execute(query)
        return ModelInstance(model_name=cls.model_name, model_content=response) if response else None

    @classmethod
    def retrieve_all(cls):
        Model.__new__(cls)
        query = Query(model_name=cls.model_name, action="retrieve", content=None)
        executor = QueryExecutor()
        response = executor.execute(query)
        return [ModelInstance(model_name=cls.model_name, model_content=response[i]) for i in response] if response else None

    @classmethod
    def filter(cls):
        Model.__new__(cls)
        pass
