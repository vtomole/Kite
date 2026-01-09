import cirq
from qiskit.synthesis import generate_basic_approximations

qubits = cirq.LineQubit.range(2)
c = cirq.Circuit(cirq.H(qubits[0]), cirq.T(qubits[0]), cirq.H(qubits[1]), cirq.T(qubits[1]), cirq.CX(qubits[0], qubits[1]), cirq.measure(qubits[1], key='a'), cirq.S(qubits[0]).with_classical_controls('a'),  cirq.X(qubits[0]).with_classical_controls('a'))


# print(c)
sim = cirq.Simulator()
result = sim.simulate(c)
# print(result)

import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.passes.synthesis import SolovayKitaev
from qiskit.quantum_info import Operator

circuit = QuantumCircuit(1)
circuit.rx(0.9, 0)
circuit.rz(0.8, 0)


print("Original circuit:")
print(circuit)

basis = ["h", "t"]
approx = generate_basic_approximations(basis, depth=3)

skd = SolovayKitaev(recursion_degree=2, basic_approximations=approx)

discretized = skd(circuit)

print("Discretized circuit:")
print(discretized)