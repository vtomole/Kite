from kite import api
from kite.api import *

circuit = api.Program(
    QREG(2),
    X(0),
    MEASURE(0))

circuit.eval()
