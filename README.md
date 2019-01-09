# Kite
Contact: vtomole@iastate.edu

# Getting started
```
kite$ pip install e .
```

``` python
import kite as kt
from kite import *

circuit = kt.Program(
    QREG(2),
    X(0),
    MEASURE(0))

print("Circuit ", circuit.run())
```

Output

```
wavefunction before measurement: 1|10>
====== MEASURE qubit 0 : 1
wavefunction after measurement: 1.0|10>

Final wavefunction:
1.0|10>

```