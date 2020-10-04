
from kite.gates import Gates
import numpy as np
def i_gen_list(num, gates):
    "Generates the tensor product of num identity gates"
    qubits = gates['qubits']

    gates = Gates.gates_set[gates['gate']]

    gates_list = []
    if len(gates) == 2:
        for _ in range(1, num):
                gates_list.append(Gates.I)

    gates_list.insert(qubits[0], gates)
    return gates_list

def kron(kron_list):
    if(len(kron_list) < 2):
        return kron_list[0]
    kron_1 = np.kron(kron_list[0], kron_list[1])
    for i in kron_list[2:]:
        kron_1 = np.kron(kron_1,kron_list[i])
    return kron_1

def create_ket(binary, num_qubits):
    a = np.zeros((2**num_qubits,1))
    a[int(binary, 2)] = 1
    return a

def amplitude(xm, C, x0):
    xm = np.asmatrix(xm)
    x0 = np.asmatrix(x0)
    res = C * xm
    return x0.getH() * res
