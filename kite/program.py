"""Defines program object"""
import sys

from kite import vm

# def H(qubit):
#     return "H " + str(qubit) + "\n"


# def QREG(num_qubits):
#     return "QUBITS " + str(num_qubits) + "\n"


# def AMPLITUDE(probability_of_amplitude):
#     return "probability_of_amplitude" + str(probability_of_amplitude) + "\n"


# def X(qubit):
#     return "X " + str(qubit) + "\n"


# def CNOT(qubit, qubit1):
#     return "CNOT " + str(qubit) + " " + str(qubit1) + "\n"


# def MEASURE(qubit):
#     return "MEASURE " + str(qubit) + "\n"

def QREG(num_qubits, probability_of_amplitude):
    if(num_qubits != len(probability_of_amplitude)):
        raise ValueError("num_qubit and probability_of_amplitude don't match")
    return {'QUBITS': num_qubits, 'probility_of_amplitude': probability_of_amplitude}

def H(qubit):
    return {'gate' :'H', 'qubits': [qubit]}

def X(qubit):
    return {'gate': 'X', 'qubits': [qubit]}

def I(qubit):
    return {'gate': 'I', 'qubits': [qubit]}

def CNOT(qubit, qubit1):
    return {'gate': 'CNOT', 'qubits': [qubit, qubit1]}

class API:
    "Provides a file API and a CLI API to the VM"

    @classmethod
    def file_api(self, file_name):
        a, b = vm.evaluate(file_name, "file")
        return a, b

    @classmethod
    def cli_api(self, instructions_string):
        a, b = vm.evaluate(instructions_string, "string")
        return a, b

class Program:
    "Consists of a list of instructions"

    def __init__(self, *instructions):
        self.instructions = list(instructions)
        # program = "". join(instructions)
        # self.instructions = program

    def get_instructions(self):
        self.check_instructions()
        return self.instructions

    def run(self):
        return API.cli_api(self.instructions)

    def run_schrodinger(self):
        return schrodinger(self.instructions)


    def check_instructions(self):
        try:
            num_qubits = self.instructions[0]['QUBITS']
        except:
            raise Exception("First instctuion should be QREG(NUM_QUBITS, probability_of_amplitude")
        for i in range(1, len(self.instructions)):
            qubits = self.instructions[i]['qubits']
            for i in qubits:
                if i >= num_qubits:
                    raise Exception("Qubit doesn't  exist to apply gate to")


if __name__ == "__main__":
    result = API.file_api(sys.argv[1])
    print(result)
