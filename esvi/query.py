class Query():
    supported_actions = ['retrieve', 'create', 'update', 'delete']

    def __init__(self, model_name, action, content):
        if action not in Query.supported_actions:
            raise Exception("Unsupported query action {}".format(action))

        self.model_name = model_name
        self.action = action
        self.content = content

    def get_action(self):
        return self.action

    def get_content(self):
        return self.content

    def get_model_name(self):
        return self.model_name
