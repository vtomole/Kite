

from kite.gates import Gates
from kite.linalg import i_gen_list, kron, create_ket, amplitude

def schrodinger(program):
    instructions = program.get_instructions()
    num_qubits = int(instructions[0]['QUBITS'])
    probability_of_amplitude = instructions[0]['probility_of_amplitude']
    a_k_0 =  '0' * num_qubits 
    g = 1    
    for i in instructions[1:]:
        gate = i_gen_list(num_qubits, i)
        g = g * kron(gate)
    return amplitude(create_ket(probability_of_amplitude, num_qubits), g, create_ket(a_k_0, num_qubits))