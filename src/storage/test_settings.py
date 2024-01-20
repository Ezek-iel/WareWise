import unittest
import settings

class TestSettings(unittest.TestCase):
    
    def test_openFile(self):
        self.assertIsNone(settings.sampleFile)

    def test_getResourceTypes(self):
        self.assertEqual(type(settings.getResourceTypes()), type([1,2]))

    def test_getProductTypes(self):
        self.assertEqual(type(settings.getProductTypes()), type([1,2]))
    
    
if __name__ == "__main__":
    unittest.main()