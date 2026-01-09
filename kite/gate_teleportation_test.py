import cirq
import numpy as np

from kite.gate_teleportation import QUBITS

r = 10
lq_0 = QUBITS[0:7]
lq_2 = QUBITS[14:21]

def test_identity_tomography():
    circuit_z = generate_logical_circuit([])
    results = qec_simulator(circuit_z, r)
    rho_11 = np.mean(results.measurements['teleported_measurements'])
    rho_00 = 1.0 - rho_11
    circuit_x = generate_logical_circuit( [cirq.H.on_each(lq_2),
             cirq.S.on_each(lq_2),
             cirq.H.on_each(lq_2)])
    results = qec_simulator(circuit_x, r)
    rho_01_im = np.mean(results.measurements['teleported_measurements']) - 0.5

    circuit_y = generate_logical_circuit( [cirq.H.on_each(lq_2),
             cirq.Y.on_each(lq_2),
             cirq.X.on_each(lq_2)])
    results = qec_simulator(circuit_y, r)
    rho_01_re = 0.5 - np.mean(results.measurements['teleported_measurements'])
    rho_01 = rho_01_re + 1j * rho_01_im
    rho_10 = np.conj(rho_01)
    rho = np.array([[rho_00, rho_01], [rho_10, rho_11]])
    tomo = TomographyResult(rho)
# q = cirq.LineQubit(0)
# c = cirq.Circuit(cirq.I(q))
# tar_rho_1 = cirq.experiments.single_qubit_state_tomography(sim, q, c, r).data
# ideal = cirq.final_density_matrix(c)
#
#

def test_logical_h_tomography():
    circuit_z = generate_logical_circuit_h([])
    results = qec_simulator(circuit_z, r)
    rho_11 = np.mean(results.measurements['teleported_measurements'])
    rho_00 = 1.0 - rho_11

    circuit_x = generate_logical_circuit_h( [cirq.H.on_each(lq_2),
            cirq.S.on_each(lq_2),
            cirq.H.on_each(lq_2)])
    results = qec_simulator(circuit_x, r)
    rho_01_im = np.mean(results.measurements['teleported_measurements']) - 0.5

    circuit_y = generate_logical_circuit_h( [cirq.H.on_each(lq_2),
            cirq.Y.on_each(lq_2),
            cirq.X.on_each(lq_2)])
    results = qec_simulator(circuit_y, r)
    rho_01_re = 0.5 - np.mean(results.measurements['teleported_measurements'])
    rho_01 = rho_01_re + 1j * rho_01_im
    rho_10 = np.conj(rho_01)
    rho = np.array([[rho_00, rho_01], [rho_10, rho_11]])

    act_rho_1 = TomographyResult(rho).data
    q = cirq.LineQubit(0)
    c = cirq.Circuit(cirq.H(q))
    ideal = cirq.final_density_matrix(c)
    print(np.allclose(act_rho_1, ideal, atol=1e-1))


# circuit_z = generate_logical_circuit_t([])
# print(circuit_z)
# results = qec_simulator_non_clifford(circuit_z, r)
# rho_11 = np.mean(results.measurements['teleported_measurements'])
# rho_00 = 1.0 - rho_11
#
# circuit_x = generate_logical_circuit_t( [cirq.H.on_each(lq_0),
#             cirq.S.on_each(lq_0),
#             cirq.H.on_each(lq_0)])
# results = qec_simulator_non_clifford(circuit_x, r)
# rho_01_im = np.mean(results.measurements['teleported_measurements']) - 0.5
#
# circuit_y = generate_logical_circuit_t( [cirq.H.on_each(lq_0),
#             cirq.Y.on_each(lq_0),
#             cirq.X.on_each(lq_0)])
# results = qec_simulator_non_clifford(circuit_y, r)
# rho_01_re = 0.5 - np.mean(results.measurements['teleported_measurements'])
# rho_01 = rho_01_re + 1j * rho_01_im
# rho_10 = np.conj(rho_01)
# rho = np.array([[rho_00, rho_01], [rho_10, rho_11]])
#
# act_rho_1 = TomographyResult(rho).data
# q = cirq.LineQubit(0)
# c = cirq.Circuit(  cirq.T(q), cirq.H(q),  cirq.X(q), cirq.T(q)  )
# ideal = cirq.final_density_matrix(c)
# print(ideal)
# print()
# print(act_rho_1)
# print(np.allclose(act_rho_1, ideal, atol=1e-1))




# circuit_z = generate_logical_circuit_t_transversal([])
# print(circuit_z)
# results = qec_simulator_non_clifford(circuit_z, r)
# rho_11 = np.mean(results.measurements['teleported_measurements'])
# rho_00 = 1.0 - rho_11
#
# circuit_x = generate_logical_circuit_t_transversal( [cirq.H.on_each(lq_0),
#             cirq.S.on_each(lq_0),
#             cirq.H.on_each(lq_0)])
# results = qec_simulator_non_clifford(circuit_x, r)
# rho_01_im = np.mean(results.measurements['teleported_measurements']) - 0.5
#
# circuit_y = generate_logical_circuit_t_transversal( [cirq.H.on_each(lq_0),
#             cirq.Y.on_each(lq_0),
#             cirq.X.on_each(lq_0)])
# results = qec_simulator_non_clifford(circuit_y, r)
# rho_01_re = 0.5 - np.mean(results.measurements['teleported_measurements'])
# rho_01 = rho_01_re + 1j * rho_01_im
# rho_10 = np.conj(rho_01)
# rho = np.array([[rho_00, rho_01], [rho_10, rho_11]])
#
# act_rho_1 = TomographyResult(rho).data
# q = cirq.LineQubit(0)
# c = cirq.Circuit(   cirq.H(q), cirq.T(q), cirq.H(q), cirq.X(q), cirq.T(q))
# ideal = cirq.final_density_matrix(c)
# print(ideal)
# print()
# print(act_rho_1)
# print(np.allclose(act_rho_1, ideal, atol=1e-1))

# circuit_z = generate_logical_circuit_cx()
# print(circuit_z)
#
# results = qec_simulator(circuit_z, r)

#print(results)


def test_compile():
    circuit = cirq.Circuit(cirq.H(QUBITS[0]))

    compile(circuit)