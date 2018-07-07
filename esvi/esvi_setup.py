from esvi.connection import Connection

class EsviSetup():
    def __init__(self) -> 'EsviSetup':
        pass

    def set_database_path(self, path: str) -> None:
        self.path = path

    def get_connection(self) -> Connection:
        if not self.path:
            raise Exception("No database path set")

        return Connection(self.path)

    def set_global_connection(self) -> None:
        global esvi_cnx
        esvi_cnx = self.get_connection()
        print(globals())
