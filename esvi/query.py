class Query():
    supported_actions = ['retrieve', 'create', 'update', 'delete', 'initialise', 'definition']

    def __init__(self, model_name, model_fields, action, content=None):
        if action not in Query.supported_actions:
            raise Exception("Unsupported query action {}".format(action))

        self.model_name = model_name
        self.action = action
        self.fields = model_fields
        self.content = content


    def get_action(self):
        return self.action

    def get_fields(self):
        return self.fields

    def get_content(self):
        return self.content

    def get_model_name(self):
        return self.model_name
