from esvi.exceptions import AdapterMethodNotImplemented # TODO

class BaseAdapter():
    def __init__(self):
        pass

    def initialise_model(self, query: Query) -> None:
      # This method is for creating a new table or equivalent in the database
      raise AdapterMethodNotImplemented()

    def create_model(self, query: Query) -> str:
      # This is for creating a row or equivalent
      raise AdapterMethodNotImplemented()

    def delete_model(self, query: Query) -> bool:
      # This is for deleting a row or equivalent in the database
      raise AdapterMethodNotImplemented()

    def retrieve_by_pk(self, query: Query) -> Optional[dict]:
      # Self explanatory
      raise AdapterMethodNotImplemented()

    def update_model(self, query: Query) -> dict:
      # Used for updating a row or equivalent in the database
      raise AdapterMethodNotImplemented()

    def filter_models(self, query: Query) -> list:
      # Used for retrieving multiple rows, in this case, the Query content contains the filters
      raise AdapterMethodNotImplemented()

    def get_model_definition(self, query: Query) -> list:
      # This is an optional method depending on the schema. In the case of sqlite3, it is used to retrieving the columns in the correct order, before performing insertion operations
      raise AdapterMethodNotImplemented()

    def retrieve_all(self, query: Query) -> list:
      # Retrieve all rows or equivalent
      raise AdapterMethodNotImplemented()
