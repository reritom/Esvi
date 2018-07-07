from typing import Optional

class Query():
    supported_actions = ['retrieve', 'create', 'update', 'delete', 'initialise', 'definition', 'all']

    def __init__(self, model_name: str, model_fields: dict, action: str, content: Optional[dict] = None) -> 'Query':
        if action not in Query.supported_actions:
            raise Exception("Unsupported query action {}".format(action))

        self.model_name = model_name
        self.action = action
        self.fields = model_fields
        self.content = content


    def get_action(self) -> str:
        return self.action

    def get_fields(self) -> dict:
        return self.fields

    def get_content(self) -> dict:
        return self.content

    def get_model_name(self) -> str:
        return self.model_name
