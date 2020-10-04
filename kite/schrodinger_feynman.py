import numpy as np
import itertools

from kite.gates import Gates
from kite.linalg import i_gen_list, kron, create_ket, amplitude
    


def multiply(num_gates, y, num_qubits, instructions):
    res = 1
    for i in range(num_gates):       
        gate = i_gen_list(num_qubits, instructions[i])
        g = kron(gate)       
        j = i + 1
        res = res * amplitude(create_ket(y[j], num_qubits), g, create_ket(y[j-1], num_qubits))
    return res


def path_integral(program):
    instructions = program.get_instructions()
    num_qubits = instructions[0]['QUBITS']
    probability_of_amplitude = instructions[0]['probility_of_amplitude']
    sum = 0
    num_gates = len(instructions[1:])
    a_k_0 =  '0' * num_qubits
    if num_gates == 1:
        res = [a_k_0, probability_of_amplitude]
        return multiply(num_gates, res, num_qubits, instructions[1:])
    else:
        res = ["".join(seq) for seq in itertools.product("01", repeat=num_qubits * (num_gates-1))]

    for j in res:  
        a_k = ([j[i:i+num_qubits] for i in range(0, len(j), num_qubits)])
        a_k.insert(0, a_k_0) 
        a_k.append(probability_of_amplitude)  
        sum = sum + multiply(num_gates, a_k, num_qubits, instructions[1:])

    return sum






