import unittest
from src.option import Option

class TestOption(unittest.TestCase):
    def test_option(self):
        option = Option("Forchetta", True)
        self.assertTrue(option.get_option() == "Forchetta")
        self.assertTrue(option.is_correct())

        option = Option("Banana", False)
        self.assertTrue(option.get_option() == "Banana")
        self.assertFalse(option.is_correct())

if __name__ == '__main__':
    unittest.main()