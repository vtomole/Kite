import pickle

import cirq
import numpy as np
import numpy.typing as npt
from cirq.experiments import TomographyResult
from mqt.qecc import CSSCode
from mqt.qecc.circuit_synthesis import LutDecoder, gate_optimal_prep_circuit

z_stabs = np.array([
    [0, 0, 0, 1, 1, 1, 1],  # Z Z Z Z I I I
    [0, 1, 1, 0, 0, 1, 1],  # Z Z I I Z Z I
    [1, 0, 1, 0, 1, 0, 1]   # Z I Z I Z I Z
])

# X stabilizer generators for the Steane code
x_stabs = np.array([
    [0, 0, 0, 1, 1, 1, 1],  # X X X X I I I
    [0, 1, 1, 0, 0, 1, 1],  # X X I I X X I
    [1, 0, 1, 0, 1, 0, 1]   # X I X I X I X
])
cc = CSSCode(3, x_stabs, z_stabs)
non_ft_sp = gate_optimal_prep_circuit(cc, zero_state=True, max_timeout=2)
q = cirq.LineQubit.range(7)
sim = cirq.Simulator()
# state = ss.converters.qiskit_to_cirq(non_ft_sp.circ)
def common_resolve(classical_data: cirq.ClassicalDataStore, key_name: str) -> bool:
    error = list(classical_data._records[cirq.MeasurementKey(name=key_name)][0])
    z_syndrome = (z_stabs @ error) % 2
    correction_index_z = lut.decode_z(z_syndrome.astype(np.int8))
    s = physical_measurements_to_logical_measurements(
                ec(error, correction_index_z)
            )
    if s == 1:
        return True
    elif s == 0:
        return False


class ZCondition(cirq.KeyCondition):
    def resolve(self, classical_data: cirq.ClassicalDataStore) -> bool:
        return common_resolve(classical_data, "ancilla0")


class XCondition(cirq.KeyCondition):
    def resolve(self, classical_data: cirq.ClassicalDataStore) -> bool:
        return common_resolve(classical_data, "ancilla1")
def logical_h(q: list[cirq.LineQubit]) -> list[cirq.GateOperation]:
    return cirq.H.on_each(q)

def logical_t(q: list[cirq.LineQubit]) -> list[cirq.GateOperation]:
    return cirq.T.on_each(q)


def logical_x(q: list[cirq.LineQubit]) -> list[cirq.GateOperation]:
    return cirq.X.on_each(q)


def logical_cx(
    q: list[cirq.LineQubit], q1: list[cirq.LineQubit]
) -> list[cirq.GateOperation]:
    return [cirq.CX(i, j) for i, j in zip(q, q1)]
def encode(qubits: list[cirq.LineQubit]) -> cirq.Circuit:
    encoding_circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.H(qubits[1]),
        cirq.H(qubits[6]),
        cirq.CNOT(qubits[6], qubits[2]),
        cirq.CNOT(qubits[1], qubits[3]),
        cirq.CNOT(qubits[0], qubits[6]),
        cirq.CNOT(qubits[2], qubits[5]),
        cirq.CNOT(qubits[0], qubits[4]),
        cirq.CNOT(qubits[1], qubits[4]),
        cirq.CNOT(qubits[5], qubits[1]),
        cirq.CNOT(qubits[4], qubits[2]))
    return encoding_circuit

QUBITS = cirq.LineQubit.range(42)

def generate_logical_circuit_cx(
) -> cirq.Circuit:
    circuit = cirq.Circuit(


        encode(QUBITS[0:7]), #0
        encode(QUBITS[7:14]), #1
        encode(QUBITS[14:21]), #2
        encode(QUBITS[21:28]), #3
        encode(QUBITS[28:35]), #4
        encode(QUBITS[35:42]), #5
        logical_h(QUBITS[7:14]), # H 1
        logical_cx(QUBITS[7:14], QUBITS[14:21]), # CX 1 2
        logical_h(QUBITS[21:28]), # H 3
        logical_cx(QUBITS[21:28], QUBITS[28:35]), # CX 3 4
        logical_cx(QUBITS[21:28], QUBITS[14:21]), # CX 3 2
        logical_cx(QUBITS[0:7], QUBITS[7:14]), # CX 0 1
        logical_h(QUBITS[0:7]), # H 0
        logical_cx(QUBITS[28:35], QUBITS[35:42]),  # CX 4 5
        logical_h(QUBITS[28:35]),  # H 4
        cirq.measure(QUBITS[0:7], key="ancilla0"), # M 0
        cirq.measure(QUBITS[7:14], key="ancilla1"), # M 1
        cirq.measure(QUBITS[28:35], key="ancilla2"),  # M 4
        cirq.measure(QUBITS[35:42], key="ancilla3"),  # M 5
        *(
            cirq.Z(QUBITS[i]).with_classical_controls(
                ZCondition(key=cirq.MeasurementKey("ancilla0"))
            )
            for i in range(14, 21)
        ), # MZ 2
        *(
            cirq.Z(QUBITS[i]).with_classical_controls(
                ZCondition(key=cirq.MeasurementKey("ancilla0"))
            )
            for i in range(21, 28) # MZ 3
        ),
        *(
            cirq.X(QUBITS[i]).with_classical_controls(
                XCondition(key=cirq.MeasurementKey("ancilla1"))
            )
            for i in range(14, 21) # MZ 2
        ),
        *(
            cirq.Z(QUBITS[i]).with_classical_controls(
                ZCondition(key=cirq.MeasurementKey("ancilla2"))
            )
            for i in range(21, 28)  # MZ 3
        ),

        *(
            cirq.X(QUBITS[i]).with_classical_controls(
                XCondition(key=cirq.MeasurementKey("ancilla3"))
            )
            for i in range(28, 35)
        ),  # MZ 4
        *(
            cirq.X(QUBITS[i]).with_classical_controls(
                XCondition(key=cirq.MeasurementKey("ancilla3"))
            )
            for i in range(35, 42)  # MZ 5
        ),
        cirq.measure(QUBITS[14:21], key="teleported_measurements_0"), # M 2
        cirq.measure(QUBITS[21:28], key="teleported_measurements_1"),  # M 3
    )

    return circuit

def generate_logical_circuit(
    logical_gate: list[cirq.Operation]
) -> cirq.Circuit:
    circuit = cirq.Circuit(
        encode(QUBITS[0:7]),
        encode(QUBITS[7:14]),
        encode(QUBITS[14:21]),
        logical_h(QUBITS[7:14]),
        logical_cx(QUBITS[7:14], QUBITS[14:21]),
        logical_cx(QUBITS[0:7], QUBITS[7:14]),
        logical_h(QUBITS[0:7]),
        #cirq.depolarize(p=0.5).on(error_qubit),
        logical_gate,
        cirq.measure(QUBITS[0:7], key="ancilla0"),
        cirq.measure(QUBITS[7:14], key="ancilla1"),
        *(
            cirq.Z(QUBITS[i]).with_classical_controls(
                ZCondition(key=cirq.MeasurementKey("ancilla0"))
            )
            for i in range(14, 21)
        ),
        *(
            cirq.X(QUBITS[i]).with_classical_controls(
                XCondition(key=cirq.MeasurementKey("ancilla1"))
            )
            for i in range(14, 21)
        ),
        cirq.measure(QUBITS[14:21], key="teleported_measurements"),
    )

    return circuit


def generate_logical_circuit_h(
    logical_gate: list[cirq.Operation], direction
) -> cirq.Circuit:

    if direction == "up":
        circuit = cirq.Circuit(
        encode(QUBITS[0:7]),
        encode(QUBITS[7:14]),
        encode(QUBITS[14:21]),
        logical_h(QUBITS[7:14]),
        logical_cx(QUBITS[7:14], QUBITS[14:21]),
        logical_cx(QUBITS[0:7], QUBITS[7:14]),
        logical_h(QUBITS[0:7]),

        logical_h(QUBITS[14:21]),
        #cirq.depolarize(p=0.5).on(error_qubit),
        logical_gate,
        cirq.measure(QUBITS[0:7], key="ancilla0"),
        cirq.measure(QUBITS[7:14], key="ancilla1"),
        *(
            cirq.X(QUBITS[i]).with_classical_controls(
                XCondition(key=cirq.MeasurementKey("ancilla0"))
            )
            for i in range(14, 21)
        ),
        *(
            cirq.Z(QUBITS[i]).with_classical_controls(
                ZCondition(key=cirq.MeasurementKey("ancilla1"))
            )
            for i in range(14, 21)
        ),
        cirq.measure(QUBITS[14:21], key="teleported_measurements"),
    )

    else:
        circuit = cirq.Circuit(
            encode(QUBITS[0:7]),
            encode(QUBITS[7:14]),
            encode(QUBITS[14:21]),


            logical_h(QUBITS[7:14]),
            logical_cx(QUBITS[14:21], QUBITS[0:7], ),
            logical_cx(QUBITS[14:21], QUBITS[7:14]),
            logical_h(QUBITS[14:21]),

            logical_h(QUBITS[0:7]),
            # cirq.depolarize(p=0.5).on(error_qubit),
            logical_gate,
            cirq.measure(QUBITS[14:21], key="ancilla0"),
            cirq.measure(QUBITS[7:14], key="ancilla1"),
            *(
                cirq.X(QUBITS[i]).with_classical_controls(
                    XCondition(key=cirq.MeasurementKey("ancilla0"))
                )
                for i in range(0, 7)
            ),
            *(
                cirq.Z(QUBITS[i]).with_classical_controls(
                    ZCondition(key=cirq.MeasurementKey("ancilla1"))
                )
                for i in range(0, 7)
            ),
            cirq.measure(QUBITS[0:7], key="teleported_measurements"),
        )

    return circuit



def generate_logical_circuit_t(
    logical_gate: list[cirq.Operation]
) -> cirq.Circuit:
    circuit = cirq.Circuit(
        encode(QUBITS[0:7]),
        encode(QUBITS[7:14]),
        encode(QUBITS[14:21]),
        logical_h(QUBITS[7:14]),
        logical_cx(QUBITS[7:14], QUBITS[14:21]),
        logical_cx(QUBITS[0:7], QUBITS[7:14]),
        logical_h(QUBITS[0:7]),

        logical_t(QUBITS[14:21]),
        #cirq.depolarize(p=0.5).on(error_qubit),
        logical_gate,
        cirq.measure(QUBITS[0:7], key="ancilla0"),
        cirq.measure(QUBITS[7:14], key="ancilla1"),
        *(
            cirq.Z(QUBITS[i]).with_classical_controls(
                ZCondition(key=cirq.MeasurementKey("ancilla0"))
            )
            for i in range(14, 21)
        ),
        *(
            cirq.S(QUBITS[i]).with_classical_controls(
                ZCondition(key=cirq.MeasurementKey("ancilla1"))
            )
            for i in range(14, 21)
        ),
        *(
            cirq.X(QUBITS[i]).with_classical_controls(
                ZCondition(key=cirq.MeasurementKey("ancilla1"))
            )
            for i in range(14, 21)
        ),
        cirq.T.on_each(QUBITS[14:21]),
        cirq.H.on_each(QUBITS[14:21]),
        cirq.X.on_each(QUBITS[14:21]),
        cirq.T.on_each(QUBITS[14:21]),
        cirq.measure(QUBITS[14:21], key="teleported_measurements"),
    )

    return circuit


def generate_logical_circuit_t_transversal(
    logical_gate: list[cirq.Operation]
) -> cirq.Circuit:
    circuit = cirq.Circuit(
        encode(QUBITS[0:7]),
        cirq.H.on_each(QUBITS[0:7]),
        cirq.T.on_each(QUBITS[0:7]),
        cirq.H.on_each(QUBITS[0:7]),
        cirq.X.on_each(QUBITS[0:7]),
        cirq.T.on_each(QUBITS[0:7]),
        logical_gate,
        cirq.measure(QUBITS[0:7], key="teleported_measurements"),
    )

    return circuit

class SerializedLutDecoder(LutDecoder):
    def __init__(self, x_lut: dict[bytes, npt.NDArray[np.int8]], z_lut: dict[bytes, npt.NDArray[np.int8]]):
        self.x_lut = x_lut
        self.z_lut = z_lut
cc = CSSCode(distance=4,  Hx=x_stabs,  Hz=z_stabs)
lut = LutDecoder(cc)
with open('steane_lut.pkl', 'wb') as f:
    pickle.dump( {'x_lut': lut.x_lut, 'z_lut': lut.z_lut}, f) # serialize the list

with open('steane_lut.pkl', 'rb') as f:
    lut_dict = pickle.load(f)

def ec(x, corrections):
    is_all_zeros = all(val == 0 for val in corrections)
    if is_all_zeros:
        return x
    return np.logical_xor(x, corrections)

lut = SerializedLutDecoder(lut_dict['x_lut'], lut_dict['z_lut'])





# correction_index_z = lut.decode_z(z_syndrome.astype(np.int8))
def mod(bits: list[np.int64], indices: list[int]) -> int:
    """Takes the 2 modulus of the bits.
    :param bits:
    :param indices:
    :return: The mod 2.
    """
    new_bits = []
    for i in indices:
        new_bits.append(bits[i])
    return int(sum(new_bits) % 2)


def physical_measurements_to_logical_measurements(
    bits: npt.NDArray[np.int_],
) -> list[int]:
    """Turns physical measurements to logical measurements.
    :param bits:
    :return: List of the logical measurements.
    """
    bits_list = list(bits)
    qubit_0 = [0, 1, 2, 3, 4, 5, 6]
    return mod(bits_list, qubit_0)
def qec_simulator(circuit: cirq.Circuit, repetitions: int) -> cirq.ResultDict:
    sim = cirq.CliffordSimulator()
    results = sim.run(circuit, repetitions=repetitions)
    new_result_dict = {}
    for key in results.measurements.keys():
        results_at_key = results.measurements[key]
        results_values = []
        for result in results_at_key:
            phys = physical_measurements_to_logical_measurements(result)
            results_values.append(phys)
        new_result_dict[key] = np.array([results_values])
    results = cirq.ResultDict(
        params=cirq.ParamResolver({}), measurements=new_result_dict
    )
    return results

def qec_simulator_non_clifford(circuit: cirq.Circuit, repetitions: int) -> cirq.ResultDict:
    sim = cirq.Simulator()
    results = sim.run(circuit, repetitions=repetitions)
    new_result_dict = {}
    for key in results.measurements.keys():
        results_at_key = results.measurements[key]
        results_values = []
        for result in results_at_key:
            phys = physical_measurements_to_logical_measurements(result)
            results_values.append(phys)
        new_result_dict[key] = np.array([results_values])
    results = cirq.ResultDict(
        params=cirq.ParamResolver({}), measurements=new_result_dict
    )
    return results


def compile(c):
    for i, op in enumerate(c.all_operations()):
        if isinstance(op.gate, cirq.HPowGate):
            print("Hadamard")
            if i % 2 == 0:
                direction = "up"
            else:
                direction = "down"
            physical_circuit = generate_logical_circuit_h([], "down")

            print(physical_circuit)


