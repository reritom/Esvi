from esvi.query import Query
from esvi.query_executor import QueryExecutor
from esvi import fields
from esvi import exceptions

class ModelInstance(dict):
    def __init__(self, model_name: str, model_fields: dict, model_content: dict) -> 'ModelInstance':

        self._model_name = model_name
        self._model_fields = model_fields
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

        print(self._model_fields)
        print(self._content)

        self.primary_key_name = self.get_primary_key()
        self._executor = QueryExecutor()

        # Any updates to the fields are stored here before being saved
        self._staged_changes = set()

        self._deleted = False

        # Used to allow setattr normally for all the above "sets" - This needs to be set at the end of init
        self._initialised = True


    def get_primary_key(self) -> str:
        for field_name in self._model_fields.keys():
            if self._model_fields[field_name].is_primary():
                return field_name

    def __iter__(self) -> dict:
        """
        To allow iteration over the content
        """
        return iter(self._content)


    def __getattr__(self, field: str):
        """
        This only gets called if the attribute isn't part of the instance. So we treat all of these are field getters
        """
        print("Getting attr {}".format(field))
        if field not in self.__dict__['_model_fields']:
            raise exceptions.InvalidFieldException("Attempting to get invalid field {0} for model {1}".format(field, self.__dict__['_model_name']))

        print("Getting field {} from content {}".format(field, self.__dict__['_content']))
        return self.__dict__['_content'][field]

    def __setattr__(self, field: str, value) -> None:
        """
        This gets called in all cases. If we are in init, we want the non-overloaded functionality, so we call the super.
        _initialised is set at the end of the init. After which, we only allow setting of existing fields.
        """
        if not '_initialised' in self.__dict__:
            # This should only happen in init
            super().__setattr__(field, value)
            return

        # At this point, we're passed init
        # only _deleted can be changed at this point
        if field == '_deleted':
            super().__setattr__(field, value)
            return

        if field not in self.__dict__['_model_fields']:
            raise exceptions.InvalidFieldException("Attempting to set invalid field {0} for model {1}".format(field, self.__dict__['_model_name']))

        if field == self.__dict__['primary_key_name']:
            raise exceptions.PrimaryKeyModificationException("Attempting to reset a primary key isn't supported")

        self.__dict__['_model_fields'][field].validate(value)
        self.__dict__['_content'][field] = value
        self.__dict__['_staged_changes'].add(field)


    def set(self, field: str, value) -> None:
        if field not in self._model_fields:
            raise exceptions.InvalidFieldException("Attempting to set invalid field {0} for model {1}".format(field, self._model_name))

        if field == self.primary_key_name:
            raise exceptions.PrimaryKeyModificationException("Attempting to reset a primary key isn't supported")

        self._model_fields[field].validate(value)
        self._content[field] = value
        self._staged_changes.add(field)

    def get(self, field: str):
        if field not in self._model_fields:
            raise exceptions.InvalidFieldException("Attempting to get invalid field {0} for model {1}".format(field, self._model_name))

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
        if self._deleted:
            print("Raising exception")
            raise exceptions.InstanceDeletedException("Attempting to save {} after deletion".format(self._model_name))

        #fields_to_update = {key: self.content[key] for key in self._staged_changes}
        query = Query(model_name=self._model_name, model_fields=self._model_fields, action="update", content=self._content)
        response = self._executor.execute(query)
        print("Saving the {0}, there are changes to fields {1}".format(self._model_name, self._staged_changes))

    def delete(self) -> bool:
        """
        Delete this model item from the DB
        Once deleted, this model instance will be unusable
        """
        query = Query(model_name=self._model_name, model_fields=self._model_fields, action="delete", content=self._content)
        response = self._executor.execute(query)
        self._deleted = True
