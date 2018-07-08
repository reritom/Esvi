from esvi.query import Query
from esvi.query_executor import QueryExecutor
from esvi import fields

class ModelInstance():
    def __init__(self, model_name: str, model_fields: dict, model_content: dict) -> 'ModelInstance':
        self.__model_name = model_name
        self.__model_fields = model_fields
        self._content = model_content

        self.__class__.__name__ = model_name + "_instance"
        self.__executor = QueryExecutor()

        # Any updates to the fields are stored here before being saved
        self._staged_changes = set()


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
