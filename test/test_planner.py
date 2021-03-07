import unittest

from georgstage.planner import Planner


class TestPlanner(unittest.TestCase):
    def setUp(self):
        self.solver = Planner()

    def test_plan(self):
        hist = []
        day = []

    def test_validate(self):
        invalid_day = []
        self.assertFalse(self.solver.is_valid(invalid_day))

if __name__ == '__main__':
    unittest.main()
