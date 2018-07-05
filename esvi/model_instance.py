from esvi.query import Query
from esvi.query_executor import QueryExecutor
from esvi import fields

class ModelInstance():
    def __init__(self, model_name, model_fields, model_content):
        # # TODO: I need to initiliase it with the primary key for committing

        self.model_name = model_name
        self.model_fields = model_fields
        self.content = model_content

        # for field_name in model_fields.key():
        #     model_fields[field_name] = field_value
        #     if field_value.__class__ == fields.PrimaryKey:
        #         self.__primary_key = self.content[field_name]

        self.__class__.__name__ = model_name + "_instance"
        self.executor = QueryExecutor()

        # Any updates to the fields are stored here before being saved
        self._staged_changes = set()

    def set(self, field, value):
        if field not in self.model_fields:
            raise Exception("Attempting to set invalid field {0} for model {1}".format(field, self.model_name))

        print("Content is {}".format(self.content))
        print("Value is {}".format(value))
        self.model_fields[field].validate(value)
        self.content[field] = value
        self._staged_changes.add(field)

    def get(self, field):
        if field not in self.model_fields:
            raise Exception("Attempting to get invalid field {0} for model {1}".format(field, self.model_name))

        return self.content[field]

    def save(self):
        #fields_to_update = {key: self.content[key] for key in self._staged_changes}
        query = Query(model_name=self.model_name, model_fields=self.model_fields, action="update", content=self.content)
        response = self.executor.execute(query)
        print("Saving the {0}, there are changes to fields {1}".format(self.model_name, self._staged_changes))

    def delete(self):
        pass
