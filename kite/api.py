import sys
import requests


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


class API:
    def __init__(self):
        self.url = 'http://localhost:5000/api/add_message/1234'

    def check_res(self, res):
        if res.ok:
            j = res.json()
            print(j["results"])
            return j
        else:
            print("res not okay")

    def run_file(self, path):
        with open(path, 'r') as myfile:
            data = myfile.read()
            res = requests.post(self.url, json={"mytext": data})

            self.check_res(res)

    def run(self, program):

        res = requests.post(self.url, json={"mytext": program})

        self.check_res(res)


class Program:
    "Consists of a list of instructions"

    def __init__(self, *instructions):
        program = "". join(instructions)

        self.instructions = program

    def eval(self):
        p = API()

        return p.run(self.instructions)


if __name__ == "__main__":

    p = API()
    p.run_file(sys.argv[1])
