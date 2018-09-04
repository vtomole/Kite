# Kite
Contact: qchackers@gmail.com

# Getting started
```
kite$ docker build -t kite .
kite$ docker run -d -p 5000:5000 kite
```

``` python
from eagle import api
from eagle.api import *

circuit = api.Program(
    QREG(1),
    X(0),
    MEASURE(0))

circuit.eval()
```

Output

```
wavefunction before measurement: 1|10>
====== MEASURE qubit 0 : 1
wavefunction after measurement: 1.0|10>

Final wavefunction:
1.0|10>

```