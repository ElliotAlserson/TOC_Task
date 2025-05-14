import unittest
from binary_increment import increment_binary

class TestBinaryIncrement(unittest.TestCase):
    def test_regular_increment(self):
        self.assertEqual(increment_binary('1011'), '1100') 
        self.assertEqual(increment_binary('1100'), '1101')
    
    def test_all_ones_case(self):
        self.assertEqual(increment_binary('1111'), '10000')
    
    def test_with_leading_zeros(self):
        self.assertEqual(increment_binary('0010'), '0011')
        self.assertEqual(increment_binary('0001'), '0010')
    
    def test_single_bit(self):
        self.assertEqual(increment_binary('0'), '1')
        self.assertEqual(increment_binary('1'), '10')
    
    def test_empty_string(self):
        self.assertEqual(increment_binary(''), '1')

if __name__ == '__main__':
    unittest.main()