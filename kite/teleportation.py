import cirq


def index_to_range(index, step=8):
    """
    Maps an index to a range with a given step size.

    Parameters:
    - index (int): The input index.
    - step (int): The size of the range step (default is 8).

    Returns:
    - range: A range object corresponding to the calculated start and end.
    """
    start = index * step
    end = start + step
    return cirq.LineQubit.range(start, end)


q0 = index_to_range(0)
q1 = index_to_range(2)


def teleported_cx(circuit, op, qubits):
    c = cirq.Circuit(
        # cirq.X(qubits[5]),
        # cirq.X(qubits[0]),
        cirq.H(qubits[3]),
        cirq.H(qubits[1]),
        cirq.CX(qubits[1], qubits[2]),
        cirq.CX(qubits[3], qubits[4]),
        cirq.CX(qubits[3], qubits[2]),
        cirq.CX(qubits[0], qubits[1]),
        cirq.H(qubits[0]),
        cirq.measure(qubits[0], key="a"),
        cirq.measure(qubits[1], key="b"),
        cirq.CX(qubits[4], qubits[5]),
        cirq.H(qubits[4]),
        cirq.measure(qubits[4], key="c"),
        cirq.measure(qubits[5], key="d"),
        cirq.Z(qubits[2]).with_classical_controls("a"),
        cirq.Z(qubits[3]).with_classical_controls("a"),
        cirq.X(qubits[2]).with_classical_controls("b"),
        cirq.Z(qubits[2]).with_classical_controls("c"),
        cirq.X(qubits[2]).with_classical_controls("d"),
        cirq.X(qubits[3]).with_classical_controls("d"),
        cirq.Moment(
            cirq.reset(qubits[0]),
            cirq.reset(qubits[1]),
            cirq.reset(qubits[4]),
            cirq.reset(qubits[5]),
        ),
    )
    return c


def gate_teleportation_compiler(circuit):
    # If qubits are in different modules, replace that physical gate with the CX teleportation circuit
    teleported_circuit = cirq.Circuit()

    circuit = circuit.transform_qubits(
        lambda q: cirq.LineQubit(16) if q.x == 1 else cirq.LineQubit(q.x)
    )

    counter = 0
    for op in circuit.all_operations():
        if isinstance(op.gate, cirq.XPowGate):
            if op.qubits[0] in q0:
                teleported_circuit = cirq.X(cirq.LineQubit(16)) + teleported_circuit
            else:
                teleported_circuit = cirq.X(cirq.LineQubit(0)) + teleported_circuit

        elif isinstance(op.gate, cirq.CXPowGate):
            if op.qubits[0] in q0 and op.qubits[1] in q1:
                if counter % 2 == 0:
                    q0_input = cirq.LineQubit(0)
                    q1_input = cirq.LineQubit(16)
                    qubits = [
                        q0_input,
                        cirq.LineQubit(7),
                        cirq.LineQubit(8),
                        cirq.LineQubit(9),
                        cirq.LineQubit(10),
                        q1_input,
                    ]
                else:
                    q0_input = cirq.LineQubit(8)
                    q1_input = cirq.LineQubit(9)
                    qubits = [
                        q0_input,
                        cirq.LineQubit(7),
                        cirq.LineQubit(0),
                        cirq.LineQubit(16),
                        cirq.LineQubit(10),
                        q1_input,
                    ]

                teleported_circuit = teleported_circuit + teleported_cx(
                    circuit, op, qubits
                )
            counter = counter + 1

    if counter % 2 == 0:
        teleported_circuit = teleported_circuit + cirq.Circuit(
            cirq.measure(cirq.LineQubit(0), key="q1"),
            cirq.measure(cirq.LineQubit(16), key="q0"),
        )
    else:
        teleported_circuit = teleported_circuit + cirq.Circuit(
            cirq.measure(cirq.LineQubit(8), key="q1"),
            cirq.measure(cirq.LineQubit(9), key="q0"),
        )

    return teleported_circuit
