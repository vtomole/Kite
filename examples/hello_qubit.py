import kite as kt

circuit = kt.Program(
    kt.QREG(2),
    kt.X(0),
    kt.MEASURE(0))

before, after = circuit.run()
print("Circuit ", after)
