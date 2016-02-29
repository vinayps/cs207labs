
import unittest
from binsearch import binary_search

import numbers
from fractions import Fraction
import numpy as np
    
class BinarySearchTests(unittest.TestCase):
    
    def test_isNumeric(self):
        with self.assertRaises(TypeError):
            binary_search(['a', 3], 3 )
                     
    def test_indexOverflow(self):
        self.assertTrue(binary_search(list(range(10)), 10) == -1)
        
    def test_zeroElements(self):
        self.assertTrue(binary_search([], 5) == -1) 
    
    def test_oneElementExists(self):
        self.assertTrue(binary_search([5], 5) == 0)
    
    def test_oneElementMissing(self):
        self.assertTrue(binary_search([5], 4) == -1)
    
    def test_twoElementExists(self):
        self.assertTrue(binary_search([5, 7], 5) == 0)
        
    def test_infExists(self):
        self.assertTrue(binary_search([1, 2, np.inf], np.inf) == 2) 
    
    def test_maxGreaterMin(self):
        self.assertTrue(binary_search(list(range(10)), 2, 3, 1) == -1)
    
    def test_maxEqualsMin(self):
        self.assertTrue(binary_search(list(range(10)), 2, 2, 2) == 2)
        

if __name__ == '__main__':
    unittest.main()