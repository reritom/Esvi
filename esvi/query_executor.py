from esvi import database_handler

class QueryExecutor():
    def __init__(self):

        if not 'esvi_cnx' in dir(database_handler):
            raise Exception("No DB connection object globalised")

        self.cnx = getattr(database_handler, 'esvi_cnx')

        print("Executor connection is {}".format(self.cnx))

    def execute(self, query):
        try:
            print("Executing query")
            self.cnx._lock()
        except Exception as e:
            print("Failed to execute query {}".format(e))
        finally:
            print("Unlocking db")
            self.cnx._unlock()

    def _get_models(self):
        pass
