import cirq

from kite.teleportation import gate_teleportation_compiler


def test_bell():
    sim = cirq.CliffordSimulator()
    qubits = cirq.LineQubit.range(17)

    physical_measurements = cirq.Circuit(
        cirq.measure(qubits[0], key="q0"), cirq.measure(qubits[1], key="q1")
    )

    c = cirq.Circuit(cirq.CX(qubits[0], qubits[1]))
    teleported_c = gate_teleportation_compiler(c)
    r = sim.run(c + physical_measurements, repetitions=10)
    teleported_r = sim.run(teleported_c, repetitions=10)
    assert r.multi_measurement_histogram(
        keys=["q0", "q1"]
    ) == teleported_r.multi_measurement_histogram(keys=["q0", "q1"])

    c = cirq.Circuit(cirq.X(qubits[1]), cirq.CX(qubits[0], qubits[1]))
    teleported_c = gate_teleportation_compiler(c)
    r = sim.run(c + physical_measurements, repetitions=10)
    teleported_r = sim.run(teleported_c, repetitions=10)
    assert r.multi_measurement_histogram(
        keys=["q0", "q1"]
    ) == teleported_r.multi_measurement_histogram(keys=["q0", "q1"])

    c = cirq.Circuit(cirq.X(qubits[0]), cirq.CX(qubits[0], qubits[1]))
    teleported_c = gate_teleportation_compiler(c)
    r = sim.run(c + physical_measurements, repetitions=10)
    teleported_r = sim.run(teleported_c, repetitions=10)
    assert r.multi_measurement_histogram(
        keys=["q0", "q1"]
    ) == teleported_r.multi_measurement_histogram(keys=["q0", "q1"])

    c = cirq.Circuit(
        cirq.X(qubits[0]), cirq.X(qubits[1]), cirq.CX(qubits[0], qubits[1])
    )
    teleported_c = gate_teleportation_compiler(c)
    r = sim.run(c + physical_measurements, repetitions=10)
    teleported_r = sim.run(teleported_c, repetitions=10)
    assert r.multi_measurement_histogram(
        keys=["q0", "q1"]
    ) == teleported_r.multi_measurement_histogram(keys=["q0", "q1"])
