from esvi.query import Query
from esvi.model_instance import ModelInstance
from esvi.query_executor import QueryExecutor

class ModelHandler():
    @classmethod
    def create(cls, **kwargs):
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
        query = Query(model_name=cls.model_name, action="retrieve", content=primary_key_value)
        executor = QueryExecutor()
        response = executor.execute(query)
        return ModelInstance(model_name=cls.model_name, model_content=response) if response else None

    @classmethod
    def retrieve_all(cls):
        query = Query(model_name=cls.model_name, action="retrieve", content=None)
        executor = QueryExecutor()
        response = executor.execute(query)
        return [ModelInstance(model_name=cls.model_name, model_content=response[i]) for i in response] if response else None

    @classmethod
    def filter(cls):
        pass
