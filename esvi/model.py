from esvi import fields
from esvi.query import Query
from esvi.model_instance import ModelInstance
from esvi.query_executor import QueryExecutor
from esvi.model_set import ModelSet

class Model():
    """
    This class is to be inherited by child models. The static methods for interacting with the DB executor also call __new__
    so that the child attributes can be retrieved without the child class needing to be instanciated first.
    """
    child_retrieved = False

    def __new__(cls, internal=False):
        print("In model new")

        # To allow the classmethods to access child properties without an explicit instanciation, this method gets called by each
        # classmethod. The following flag checks whether it has already been ran or not
        if cls.child_retrieved == True and internal == True:
            return

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

        cls.executor = QueryExecutor()
        return cls


    @classmethod
    def get_fields(cls):
        """
        Return a dictionary with the field names and their field classes
        """
        Model.__new__(cls, internal=True)
        return cls.model_fields

    @classmethod
    def _initialise_in_db(cls):
        """
        This will add the model definition to the DB
        """
        Model.__new__(cls, internal=True)
        # Here we create the query and pass it to the executor
        query = Query(model_name=cls.model_name, model_fields=cls.model_fields, action="initialise")
        response = cls.executor.execute(query)

    @classmethod
    def _get_defition_from_db(cls):
        """
        Retrieves the model fields from the DB in a list of field names in the correct order
        """
        Model.__new__(cls, internal=True)
        # Here we create the query and pass it to the executor
        query = Query(model_name=cls.model_name, model_fields=None, action="definition")
        response = cls.executor.execute(query)

    @classmethod
    def create(cls, **kwargs):
        """
        Create a model item in the DB
        """
        Model.__new__(cls, internal=True)

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
        query = Query(model_name=cls.model_name, model_fields=cls.model_fields, action="create", content=content)
        response = cls.executor.execute(query)
        return ModelInstance(model_name=cls.model_name, model_fields=cls.model_fields, model_content=response) if response else None

    @classmethod
    def retrieve(cls, primary_key_value):
        """
        Retrieve a single model by primary key
        """
        Model.__new__(cls, internal=True)
        query = Query(model_name=cls.model_name, model_fields=cls.model_fields, action="retrieve", content=primary_key_value)
        response = cls.executor.execute(query)
        return ModelInstance(model_name=cls.model_name, model_fields=cls.model_fields, model_content=response) if response else None

    @classmethod
    def retrieve_all(cls):
        """
        Retrieve all of the model items from the db and returns them in a model set
        """
        Model.__new__(cls, internal=True)
        query = Query(model_name=cls.model_name, model_fields=cls.model_fields, action="all")
        response = cls.executor.execute(query)
        print("Retrieve all response is {}".format(response))
        return ModelSet([ModelInstance(model_name=cls.model_name, model_fields=cls.model_fields, model_content=i) for i in response]) if response else None

    @classmethod
    def filter(cls, **kwargs):
        Model.__new__(cls, internal=True)

        filters = ['_less_or_equal',
                   '_greater_or_equal',
                   'equal',
                   '_less_than',
                   '_greater_than',
                   'between_inc',
                   'between',
                   'not']
        pass
