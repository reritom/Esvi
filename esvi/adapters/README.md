# Adapters

Adapters are used for creating the interface with an array of different database schemas.
Each adapter has follows a defined API structure which gets called by the query executor.
An adapter gets initialised with the Connection object, which allows the adapter to have access to the database path.
Each of the adapter methods which get called by the QueryExecutor are passed a Query object, which contains the model name, the fields, and the field content.

## Adapter methods
In the following methods, if they return a dictionary, it a dict of field_names and field_values representing the row or equivalent.
If it returns a list, it is a list of the dictionary just described.
In the case of creation, the string is the rowid or equivalent. But this might change to a boolean instead

```
def initialise_model(self, query: Query) -> None:
  # This method is for creating a new table or equivalent in the database

def create_model(self, query: Query) -> str:
  # This is for creating a row or equivalent

def delete_model(self, query: Query) -> bool:
  # This is for deleting a row or equivalent in the database

def retrieve_by_pk(self, query: Query) -> Optional[dict]:
  # Self explanatory

def update_model(self, query: Query) -> dict:
  # Used for updating a row or equivalent in the database

def filter_models(self, query: Query) -> list:
  # Used for retrieving multiple rows, in this case, the Query content contains the filters

def get_model_definition(self, query: Query) -> list:
  # This is an optional method depending on the schema. In the case of sqlite3, it is used to retrieving the columns in the correct order, before performing insertion operations

def retrieve_all(self, query: Query) -> list:
  # Retrieve all rows or equivalent
```
