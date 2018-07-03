import unittest, os

class TestEsvicoreAdapter(unittest.TestCase):

    def setUp(self):
        self.test_database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.esvi')

        if os.path.exists(self.test_database_path):
            os.remove(self.test_database_path)

        with open(self.test_database_path, 'w') as f:
            f.write('')
            

    def tearDown(self):
        print("In teardown")

if __name__=='__main__':
    unittest.main()
