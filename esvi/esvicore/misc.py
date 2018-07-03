# These are to be used when interacting with an escvicore db
''' DO NOT IMPORT THIS, CODE TO BE PLACED ELSEWHERE'''

    def _lock(self):
        lock_path = os.path.join(self.database_dir, '.esvi.lock')
        if os.path.isfile(lock_path):
            with open(lock_path, 'r') as f:
                lock_file = f.read()

            try:
                lock_file = json.loads(lock_file)
            except:
                print("Failed to read lock json")
                os.remove(lock_path)
            return

            # Here we will check if there has been a timeout

        lock_bom = {'locked_at': datetime.datetime.now().isoformat(),
                    'locked_by': self.session_id,
                    'db_identifier': self.database_path}

        with open(lock_path, 'w') as f:
            f.write(json.dumps(lock_bom))

    def _unlock(self):
        lock_path = os.path.join(self.database_dir, '.esvi.lock')
        if os.path.isfile(lock_path):
            with open(lock_path, 'r') as f:
                lock_file = f.read()

            lock_bom = json.loads(lock_file)

            if lock_bom.get('locked_by', None) == self.session_id:
                print("Deleting the lock")
                os.remove(lock_path)
