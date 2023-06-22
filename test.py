import unittest
from pon2 import load, loads


class TestStringMethods(unittest.TestCase):

    def test_loads(self):
        pon_text = '''
            {
             'python': False,
             "json": None,
             "set": {1, 2, 3, "set"}, 
             "tuple": ("tuple", 1, 2, 3), 
              False: "Test key", 
              True: frozenset({"set"}),
              "numbers": [1, 1.0, 0x1, 0o1, 0b1] # int, float, hex, octal, binary
            }'''
        pon_dict = {
            'python': False,
            "json": None,
            "set": {1, 2, 3, "set"},
            "tuple": ("tuple", 1, 2, 3),
            False: "Test key",
            True: frozenset({"set"}),
            "numbers": [1, 1.0, 0x1, 0o1, 0b1],
        }
        self.assertEqual(loads(pon_text), pon_dict)

    def test_load(self):
        pon_dict = {
            'python': False,
            "json": None,
            "set": {1, 2, 3, "set"},
            "tuple": ("tuple", 1, 2, 3),
            False: "Test key",
            True: frozenset({"set"}),
            "numbers": [1, 1.0, 0x1, 0o1, 0b1],
        }
        with open("test.pon") as f:
            self.assertEqual(load(f), pon_dict)


if __name__ == '__main__':
    unittest.main()
