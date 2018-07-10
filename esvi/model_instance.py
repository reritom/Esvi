from esvi.query import Query
from esvi.query_executor import QueryExecutor
from esvi import fields

class ModelInstance():
    def __init__(self, model_name: str, model_fields: dict, model_content: dict, construct_foreigns=False) -> 'ModelInstance':
        self.__model_name = model_name
        self.__model_fields = model_fields
        self._content = {}

        # The content contains primary keys for foreign models, so here we need to construct these foreign models
        for model_field_name in model_fields:
            if model_fields[model_field_name].is_foreign():
                reference_model = model_fields[model_field_name].get_reference()
                primary_key = reference_model.get_primary_key()

                # Now we get the value for this primary key from the content and retrieve the model instance
                retrieved_instance = reference_model.retrieve(model_content[primary_key])
                self._content[model_field_name] = retrieved_instance
                continue

            self._content[model_field_name] = model_content[model_field_name]

        print(self.__model_fields)
        print(self._content)
        self.__executor = QueryExecutor()

        # Any updates to the fields are stored here before being saved
        self._staged_changes = set()

    def get_primary_key(self) -> str:
        for field_name in self.__model_fields.keys():
            if self.__model_fields[field_name].is_primary():
                return field_name

    def __iter__(self) -> dict:
        # To allow iteration over the content
        return iter(self._content)

    def set(self, field: str, value) -> None:
        if field not in self.__model_fields:
            raise Exception("Attempting to set invalid field {0} for model {1}".format(field, self.__model_name))

        #TODO, here I need to make sure the primary key isnt being changed

        self.__model_fields[field].validate(value)
        self._content[field] = value
        self._staged_changes.add(field)

    def get(self, field: str):
        if field not in self.__model_fields:
            raise Exception("Attempting to get invalid field {0} for model {1}".format(field, self.__model_name))

        print("Getting field {} from content {}".format(field, self._content))
        return self._content[field]

    def pretty(self) -> None:
        print()
        for key, value in self._content.items():
            print('{}: {}'.format(key, value))

    def save(self) -> bool:
        """
        Update all of the rows for this model item in the db
        """
        #fields_to_update = {key: self.content[key] for key in self._staged_changes}
        query = Query(model_name=self.__model_name, model_fields=self.__model_fields, action="update", content=self._content)
        response = self.__executor.execute(query)
        print("Saving the {0}, there are changes to fields {1}".format(self.__model_name, self._staged_changes))

    def delete(self) -> bool:
        """
        Delete this model item from the DB
        Once deleted, this model instance will be unusable
        """
        query = Query(model_name=self.__model_name, model_fields=self.__model_fields, action="delete", content=self._content)
        response = self.__executor.execute(query)
