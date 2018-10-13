import kite as kt
from kite import *

circuit = kt.Program(
    QREG(2),
    X(0),
    MEASURE(0))

circuit.eval()
