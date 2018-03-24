import numpy as np
import cmath
class Gates:
    "Contains basic quantum gates"

    #Rotation
    def RX(self, theta):
        return np.matrix([[round(np.cos(theta/ 2 )), np.around(-1j * np.sin(theta / 2))],
                          [np.around(-1j * np.sin(theta / 2)), np.around(np.cos(theta/ 2 ))]])

    def RY(self, theta):
        return np.matrix([[np.cos(theta/ 2 ),  np.sin(theta / 2)],
                          [-1j * np.sin(theta / 2), np.cos(theta/ 2 )]])

    def RZ(self, theta):
        return np.matrix([[np.exp(-1j * theta / 2),  0],
                          [0, np.exp(1j * theta / 2)]])

    #pauli
    I = np.matrix([[1, 0], [0, 1]])
    X = np.matrix([[0, 1], [1, 0]])
    Y = np.matrix([[0, 0 - 1j], [0 + 1j, 0]])
    Z = np.matrix([[1, 0], [0, -1]])

    #universal gates
    H = (X + Z)/np.sqrt(2)
    T = np.matrix([[1, 0], [0, cmath.exp(1j * np.pi / 4)]])
    S = np.matrix([[1.0, 0.0], [0.0, 1.0j]])
    CNOT = np.matrix([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1],
                      [0, 0, 1, 0]])

    #miscellaneous
    CZ = np.matrix([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, -1]])
    SWAP = np.matrix([[1, 0, 0, 0],
                      [0, 0, 1, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1]])
