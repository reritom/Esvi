class ModelInstance():
    def __init__(self, model_name, model_fields, model_content):
        # # TODO: I need to initiliase it with the primary key for committing

        self.name = model_name
        self.fields = model_fields
        self.content = model_content

        self.__class__.__name__ = model_name + "_instance"

        # Any updates to the fields are stored here before being saved
        self._staged_changes = set()

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

    def delete(self):
        pass
