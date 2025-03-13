import unittest


def add_function(a,b):
    return a + b

class TestAddFunction(unittest.TestCase):
    def test1(self):
        self.assertEqual(add_function(1,2),3)
    def test2(self):
        self.assertEqual(add_function(1,-7),-6)
    def test3(self):
        self.assertEqual(add_function(1,2),3)
    def test4(self):
        self.assertEqual(add_function(1,2),3)
    def test5(self):
        self.assertEqual(add_function(1,2),3)
    def test6(self):
        self.assertEqual(add_function(1,2),3)
    def test7(self):
        self.assertEqual(add_function(2,3),5)


if __name__ == '__main__':
    unittest.main()
