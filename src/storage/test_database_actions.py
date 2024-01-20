import database_actions
import unittest

class TestDB(unittest.TestCase):

    tablenames = ["resources","suppliers","products"]

    def test_checkConnection(self):
        self.assertIsNotNone(database_actions.sampleConnection)

    def test_getAllData(self):
        checks = []
        for name in self.tablenames:
            if database_actions.getallData(name) != None :
                    checks.append(True)
            else:
                checks.append(False)
        return self.assertEqual(False not in checks, True)
    
    def test_getdate(self):
         return self.assertEqual(type(database_actions.get_date()), type("samplestring"))



if __name__ == "__main__":
    unittest.main()