class Program:
    "Consists of a list of instructions"

    def __init__(self, *instructions):
        program = "". join(instructions)

        self.instructions = program

    def eval(self):
        p = API()

        return p.run(self.instructions)

def run(instructions):
    p = Program(instructions)
    return p.eval()
