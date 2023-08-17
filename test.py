import unittest
from pon2 import loader


class TestStringMethods(unittest.TestCase):
    test_dict = {
        "PON2": True,
        "json": False,
        "str": "str",
        "Nothing": None,
        0: "0",
        # Type can be a key
        tuple: (tuple([1]), (1, 1)),
        list: [list([1]), [1]],
        dict: [{"key": "value"}, dict(key="value")], # dict support ONLY hashable types as KEY
        set: [set([1, 2, 3]), {1, 2, 3}],
        frozenset: frozenset(), # frozenset
        "numbers": [1, 1.0, 0x1, 0o1, 0b1], # int, float, hex, octal, binary
        "callables": [
            str(0), 
            int(0), 
            bool(0), 
            float(0), 
            dict(k=0), 
            list([0]), 
            tuple([0]), 
            set([0]), 
            frozenset([0])
        ]
    }

    def test_loads(self):
        with open("test.pon") as f:
            pon_text = f.read()
        self.assertEqual(loader.loads(pon_text), self.test_dict)

    def test_load(self):
        with open("test.pon") as f:
            self.assertEqual(loader.load(f), self.test_dict)


if __name__ == '__main__':
    unittest.main()
