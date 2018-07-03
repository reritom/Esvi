from esvi import esvi_setup

class QueryExecutor():
    adapters = {'esvi': adapters.esvicore_adapter.EsvicoreAdapter,
                'sqlite3': adapters.sqlite3_adapter.Sqlite3Adapter}

    def __init__(self):

        if not 'esvi_cnx' in dir(esvi_setup):
            raise Exception("No DB connection object globalised")

        # Retrieve the global connection
        self.cnx = getattr(esvi_setup, 'esvi_cnx')

        # Set the correct adapter
        self.adapter = QueryExecutor.adapters(self.cnx.get_database_type())(self.cnx)

        print("Executor connection is {}".format(self.cnx))

    def execute(self, query):
        """
        Here we will route the queries to the correct adapter
        """
        router = {'retrieve': self.adapter.retrieve,
                  'create': self.adapter.create,
                  'update': self.adapter.update,
                  'delete': self.adapter.delete,
                  'filter': self.adapter.filter}

        router[query.get_action](query)
