import unittest
from cfg_to_cnf import cfg_to_cnf

class TestCFGtoCNF(unittest.TestCase):
    def test_sample_grammar_conversion(self):
        """Test the exact grammar example from the original code"""
        grammar = {
            'S': ['aB', 'bA', 'A'],
            'A': ['a', 'aS', 'bAA'],
            'B': ['b', 'bS', 'aBB']
        }
        
        result = cfg_to_cnf(grammar)
        
        # Verify all productions are in CNF format
        for lhs, prods in result.items():
            for prod in prods:
                self.assertTrue(len(prod) == 1 or len(prod) == 2,
                              f"Production {lhs} → {prod} violates CNF")
                
        # Verify specific expected transformations
        self.assertIn('S', result)
        self.assertIn('A', result)
        self.assertIn('B', result)
        
        # Check terminal replacements exist
        terminal_vars = [var for var in result if var.startswith('T')]
        self.assertTrue(len(terminal_vars) >= 2)  # At least T0 and T1
        
        # Check for split productions
        split_vars = [var for var in result if var.startswith('N')]
        self.assertTrue(len(split_vars) > 0)

if __name__ == '__main__':
    unittest.main()