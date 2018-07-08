from esvi.connection import Connection

class EsviSetup():
    STRICT_MODE = "STRICT"
    LIBERAL_MODE = "LIBERAL"

    def __init__(self) -> 'EsviSetup':
        self.mode = EsviSetup.LIBERAL_MODE
        pass

    def set_database_path(self, path: str) -> None:
        self.path = path

    def get_connection(self) -> Connection:
        if not self.path:
            raise Exception("No database path set")

        return Connection(self.path)

    def set_strict_mode(self) -> None:
        """
        Strict mode raises exceptions in some cases, such as failing to retrieve by PK
        """
        self.mode = EsviSetup.STRICT_MODE

    def set_liberal_mode(self) -> None:
        """
        Liberal mode skips some exceptions and returns None instead
        """
        self.mode = EsviSetup.LIBERAL_MODE

    def get_mode(self) -> str:
        return self.mode

    def set_global_connection(self) -> None:
        global esvi_cnx
        esvi_cnx = self.get_connection()
        print(globals())
