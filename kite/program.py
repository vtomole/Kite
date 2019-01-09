"""Defines program object"""
from kite import vm

def H(qubit):
    return "H " + str(qubit) + "\n"


def QREG(num_qubits):
    return "QUBITS " + str(num_qubits) + "\n"


def X(qubit):
    return "X " + str(qubit) + "\n"


def CNOT(qubit, qubit1):
    return "CNOT " + str(qubit) + " " + str(qubit1) + "\n"


def MEASURE(qubit):
    return "MEASURE " + str(qubit) + "\n"


class Program:
    "Consists of a list of instructions"

    def __init__(self, *instructions):
        program = "". join(instructions)

        self.instructions = program
        
    def run(self):
        return vm.evaluate(self.instructions, "string")[1]
        
