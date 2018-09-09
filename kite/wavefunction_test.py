from program import run
from .vm import wavefunction


def test_bell_states():
    epr_program = 'QUBITS 2\nH 0\nCNOT 0 1'
    print(run(epr_program)[1])
    assert run(epr_program)[1] == "0.71|00> + 0.71|11>"
