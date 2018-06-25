import os, json, uuid, datetime, time

class Esvi():

    def __enter__(self):
        print("Entering the ESVI context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting ESVI")

    def _lock(self):
        lock_path = os.path.join(self.this_dir, '.esvi.lock')
        if os.path.isfile(lock_path):
            with open(lock_path, 'r') as f:
                lock_file = f.read()

            try:
                lock_file = json.loads(lock_file)
            except:
                print("Failed to read lock json")
            return

            # Here we will check if there has been a timeout

        self.session_id = str(uuid.uuid4())

        lock_bom = {'locked_at': datetime.datetime.now().isoformat(),
                    'locked_by': self.session_id,
                    'db_identifier': self.db_path}

        with open(lock_path, 'w') as f:
            f.write(json.dumps(lock_bom))

    def _unlock(self):
        lock_path = os.path.join(self.this_dir, '.esvi.lock')
        if os.path.isfile(lock_path):
            with open(lock_path, 'r') as f:
                lock_file = f.read()

            lock_bom = json.loads(lock_file)

            if lock_bom.get('locked_by', None) == self.session_id:
                os.remove(lock_path)

    def __init__(self):
        """
        We will search for any db at this level, else we'll set a flag requiring a manual setup
        """

        self.this_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = self._discover_in_dir(self.this_dir)

    def _discover_in_dir(self, dir_path):
        """
        Search this dir for any esvi dbs
        """
        for this_file in os.listdir(dir_path):
            if this_file.endswith('.esvi'):
                return os.path.join(dir_path, this_file)

        return None

    def create_db(self, path):
        """
        Check if the db already exists
        Initialise an empty db
        """
        if os.path.isfile(path):
            print("DB already exists")
            return

        self.db_path = path

        print("Opening the base db")
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'basedb.txt'), 'r') as f:
            base = f.read()
            print("Reading the base as {0}".format(base))

    def retrieve_models(self):
        pass

    def add_model(self):
        pass

    def delete_model(self):
        pass





        pass

    @staticmethod
    def check_integrity(db_path):
        pass
