from esvi import esvi_setup
from esvi.adapters.esvicore_adapter import EsvicoreAdapter
from esvi.adapters.sqlite3_adapter import Sqlite3Adapter

class QueryExecutor():
    adapters = {'esvi': EsvicoreAdapter,
                'sqlite3': Sqlite3Adapter}

    def __init__(self):
        if not 'esvi_cnx' in dir(esvi_setup):
            raise Exception("No DB connection object globalised")

        # Retrieve the global connection
        self.cnx = getattr(esvi_setup, 'esvi_cnx')

        # Set the correct adapter
        self.adapter = QueryExecutor.adapters[self.cnx.get_database_type()](self.cnx)

        print("Executor connection is {}".format(self.cnx))

    def execute(self, query):
        """
        Here we will route the queries to the correct adapter
        """

        router = {'retrieve': self.adapter.retrieve_by_pk,
                  'all': self.adapter.retrieve_all,
                  'create': self.adapter.create_model,
                  'update': self.adapter.update_model,
                  'delete': self.adapter.delete_model,
                  'filter': self.adapter.filter_models,
                  'initialise': self.adapter.initialise_model,
                  'definition': self.adapter.get_model_definition}

        return router[query.get_action()](query)
