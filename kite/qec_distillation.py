import cirq
import numpy as np


def encode(qubits: list[cirq.LineQubit]) -> cirq.Circuit:
    encoding_circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.H(qubits[1]),
        cirq.H(qubits[3]),
        cirq.CX(qubits[0], qubits[2]),
        cirq.CX(qubits[3], qubits[5]),
        cirq.CX(qubits[1], qubits[6]),
        cirq.CX(qubits[0], qubits[4]),
        cirq.CX(qubits[3], qubits[6]),
        cirq.CX(qubits[1], qubits[5]),
        cirq.CX(qubits[0], qubits[6]),
        cirq.CX(qubits[1], qubits[2]),
        cirq.CX(qubits[3], qubits[4]),
    )
    return encoding_circuit


top_qubits = cirq.LineQubit.range(7)
bottom_qubits = cirq.LineQubit.range(7, 14)
top_ancilla_qubits = cirq.LineQubit.range(14, 20)
bottom_ancilla_qubits = cirq.LineQubit.range(20, 26)

c = cirq.Circuit(
    cirq.H.on_each(top_qubits),
    cirq.CX(top_qubits[0], bottom_qubits[0]),
    cirq.CX(top_qubits[1], bottom_qubits[1]),
    cirq.CX(top_qubits[2], bottom_qubits[2]),
    cirq.CX(top_qubits[3], bottom_qubits[3]),
    cirq.CX(top_qubits[4], bottom_qubits[4]),
    cirq.CX(top_qubits[5], bottom_qubits[5]),
    cirq.CX(top_qubits[6], bottom_qubits[6]),
)

c = c.with_noise(cirq.depolarize(p=0.1))

c.append(cirq.H.on_each(top_ancilla_qubits))

c.append([cirq.CX(top_ancilla_qubits[0], top_qubits[0]), cirq.CX(top_ancilla_qubits[0], top_qubits[1]), cirq.CX(top_ancilla_qubits[0], top_qubits[2]), cirq.CX(top_ancilla_qubits[0], top_qubits[3])])
c.append([cirq.CX(top_ancilla_qubits[1], top_qubits[0]), cirq.CX(top_ancilla_qubits[1], top_qubits[1]), cirq.CX(top_ancilla_qubits[1], top_qubits[4]), cirq.CX(top_ancilla_qubits[1], top_qubits[5])])
c.append([cirq.CX(top_ancilla_qubits[2], top_qubits[0]), cirq.CX(top_ancilla_qubits[2], top_qubits[2]), cirq.CX(top_ancilla_qubits[2], top_qubits[4]), cirq.CX(top_ancilla_qubits[2], top_qubits[6])])
c.append([cirq.CZ(top_ancilla_qubits[3], top_qubits[0]), cirq.CZ(top_ancilla_qubits[3], top_qubits[1]), cirq.CZ(top_ancilla_qubits[3], top_qubits[2]), cirq.CZ(top_ancilla_qubits[3], top_qubits[3])])
c.append([cirq.CZ(top_ancilla_qubits[4], top_qubits[0]), cirq.CZ(top_ancilla_qubits[4], top_qubits[1]), cirq.CZ(top_ancilla_qubits[4], top_qubits[4]), cirq.CZ(top_ancilla_qubits[4], top_qubits[5])])
c.append([cirq.CZ(top_ancilla_qubits[5], top_qubits[0]), cirq.CZ(top_ancilla_qubits[5], top_qubits[2]), cirq.CZ(top_ancilla_qubits[5], top_qubits[4]), cirq.CZ(top_ancilla_qubits[5], top_qubits[6])])
c.append(cirq.H.on_each(top_ancilla_qubits))
c.append(cirq.measure(top_ancilla_qubits, key='top_bell_pairs'))
c.append([cirq.reset(top_ancilla_qubits[0]), cirq.reset(top_ancilla_qubits[1]), cirq.reset(top_ancilla_qubits[2]), cirq.reset(top_ancilla_qubits[3]) ,cirq.reset(top_ancilla_qubits[4]) , cirq.reset(top_ancilla_qubits[5]) ])
c.append(cirq.H.on_each(top_ancilla_qubits))
c.append([cirq.CX(top_ancilla_qubits[0], bottom_qubits[0]), cirq.CX(top_ancilla_qubits[0], bottom_qubits[1]), cirq.CX(top_ancilla_qubits[0], bottom_qubits[2]), cirq.CX(top_ancilla_qubits[0], bottom_qubits[3])])
c.append([cirq.CX(top_ancilla_qubits[1], bottom_qubits[0]), cirq.CX(top_ancilla_qubits[1], bottom_qubits[1]), cirq.CX(top_ancilla_qubits[1], bottom_qubits[4]), cirq.CX(top_ancilla_qubits[1], bottom_qubits[5])])
c.append([cirq.CX(top_ancilla_qubits[2], bottom_qubits[0]), cirq.CX(top_ancilla_qubits[2], bottom_qubits[2]), cirq.CX(top_ancilla_qubits[2], bottom_qubits[4]), cirq.CX(top_ancilla_qubits[2], bottom_qubits[6])])
c.append([cirq.CZ(top_ancilla_qubits[3], bottom_qubits[0]), cirq.CZ(top_ancilla_qubits[3], bottom_qubits[1]), cirq.CZ(top_ancilla_qubits[3], bottom_qubits[2]), cirq.CZ(top_ancilla_qubits[3], bottom_qubits[3])])
c.append([cirq.CZ(top_ancilla_qubits[4], bottom_qubits[0]), cirq.CZ(top_ancilla_qubits[4], bottom_qubits[1]), cirq.CZ(top_ancilla_qubits[4], bottom_qubits[4]), cirq.CZ(top_ancilla_qubits[4], bottom_qubits[5])])
c.append([cirq.CZ(top_ancilla_qubits[5], bottom_qubits[0]), cirq.CZ(top_ancilla_qubits[5], bottom_qubits[2]), cirq.CZ(top_ancilla_qubits[5], bottom_qubits[4]), cirq.CZ(top_ancilla_qubits[5], bottom_qubits[6])])



c.append(cirq.H.on_each(top_ancilla_qubits))
c.append(cirq.measure(top_qubits, key='lq_0'))
c.append(cirq.measure(bottom_qubits, key='lq_1'))

c.append(cirq.measure(top_ancilla_qubits, key='bottom_bell_pairs'))


def test_bell(c, repetitions):
    sim = cirq.CliffordSimulator()

    for i in range(repetitions):
        while True:
            res = sim.run(c, repetitions=1)
            if np.array_equal(res.measurements['top_bell_pairs'],  np.array([[0, 0, 0, 0, 0, 0]])) and np.array_equal(res.measurements['bottom_bell_pairs'],  np.array([[0, 0, 0, 0, 0, 0]])):
                if sum(res.measurements['lq_0'][0]) %2 == sum(res.measurements['lq_1'][0]) % 2:
                    return True
                break
    return False
print(c)
print(test_bell(c, 100))