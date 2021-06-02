import unittest
from vectormath import Vector3


class TestVectors(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector3(1.0, -2.0, -2.0)
        self.v2 = Vector3(3.0, 6.0, 9.0)

    def test_magnitude(self):
        self.assertEqual(self.v1.magnitude(), 3)

    def test_addition(self):
        sum = self.v1 + self.v2
        self.assertEqual(getattr(sum, "x"), 4.0)

    def test_multiplication(self):
        sum = self.v1 * 2
        self.assertEqual(getattr(sum, "x"), 2.0)


if __name__ == "__main__":
    unittest.main()
