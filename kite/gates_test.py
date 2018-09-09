from .gates import Gates
import numpy as np


def test_base_gate_matrices():
    "Test the gates which are hardcoded matrices"
    g = Gates()
    # I
    assert np.isclose(Gates.I, np.eye(2)).all()
