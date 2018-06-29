class ModelInstance():
    def __init__(self, model_name, model_content):
        self.name = model_name
        self.fields = model_fields
        self.content = model_content

        # Any updates to the fields are stored here before being saved
        self._staged_changes = set()
        pass

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
