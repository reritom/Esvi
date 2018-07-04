from esvi import esvi_setup
from esvi.adapters.esvicore_adapter import EsvicoreAdapter
from esvi.adapters.sqlite3_adapter import Sqlite3Adapter

class QueryExecutor():
    adapters = {'esvi': EsvicoreAdapter,
                'sqlite': Sqlite3Adapter}

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

        router = {'retrieve': self.adapter.retrieve,
                  'create': self.adapter.create,
                  'update': self.adapter.update,
                  'delete': self.adapter.delete,
                  'filter': self.adapter.filter,
                  'initialise': self.adapter.initialise,
                  'definition': self.adapter.get_models}

        router[query.get_action()](query, self.cnx)
