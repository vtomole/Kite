import unittest
import numpy as np
from kite.gates import Gates


class test_gates(unittest.TestCase):
    
    def test_base_gate_matrices(self):
        "Test the gates which are hardcoded matrices"
        g = Gates()
        assert np.isclose(g.I, np.eye(2)).all()


if __name__ == '__main__':
    unittest.main()