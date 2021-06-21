import unittest
from src.timer import Timer

class TestTimer(unittest.TestCase):
    def test_timer(self):
        timer = Timer(2)
        self.assertTrue(timer.get_remaining_time() == 2)
        self.assertFalse(timer.is_timer_over())
        timer.start()
        self.assertTrue(timer.get_remaining_time() == 0)
        self.assertTrue(timer.is_timer_over())

if __name__ == '__main__':
    unittest.main()

