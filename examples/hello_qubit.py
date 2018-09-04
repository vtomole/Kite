from eagle import api
from eagle.api import *

circuit = api.Program(
    QREG(2),
    X(0),
    MEASURE(0))

circuit.eval()
