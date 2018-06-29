from esvi.query_executor import QueryExecutor
from esvi.query import Query
from esvi.model_instance import ModelInstance

class ModelHandler():
    def __init__(self, model_name, model_fields):
        self.model_name = model_name
        self.model_fields = model_fields

        self.executor = QueryExecutor()


    def create(self, **kwargs):
        # Initialise the content of this model
        content = dict()

        # Here we validate that the model is being initialised with enough information
        for field_name, definition in self.model_fields.items():
            # Check if it is in the kwargs
            if field_name in kwargs:
                # TODO validate that the kwarg is correct type for the field
                definition.validate(kwargs[field_name])
                content[field_name] = kwargs[field_name]

            # Check if it has a default value
            elif definition.has_default():
                content[field_name] = definition.get_default()

            else:
                raise Exception("{} missing as parameter and has no default".format(field_name))

        # Here we create the query and pass it to the executor
        query = Query(model_name=self.model_name, action="create", content=content)
        response = self.executor.execute(query)
        return ModelInstance(model_name=self.model_name, model_content=response) if response else None

    def retrieve(self, primary_key_value):
        query = Query(model_name=self.model_name, action="retrieve", content=primary_key_value)
        response = self.executor.execute(query)
        return ModelInstance(model_name=self.model_name, model_content=response) if response else None

    def retrieve_all(self):
        query = Query(model_name=self.model_name, action="retrieve", content=None)
        response = self.executor.execute(query)
        return [ModelInstance(model_name=self.model_name, model_content=response[i]) for i in response] if response else None

    def filter(self):
        pass
