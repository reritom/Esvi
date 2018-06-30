from esvi import access_setup

class QueryExecutor():
    def __init__(self):

        if not 'esvi_cnx' in dir(access_setup):
            raise Exception("No DB connection object globalised")

        self.cnx = getattr(access_setup, 'esvi_cnx')

        print("Executor connection is {}".format(self.cnx))

    def execute(self, query):
        print("Executing query")

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
