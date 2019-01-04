import sys
import requests

from kite import vm


def H(qubit):
    return "H " + str(qubit) + "\n"


def QREG(n):
    return "QUBITS " + str(n) + "\n"


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

    def eval(self):
        p = API()

        return p.run(self.instructions)
    
    def run(self):
         a, b = vm.evaluate(self.instructions, "string")
         print(b)


if __name__ == "__main__":

    p = API()
    p.run_file(sys.argv[1])
