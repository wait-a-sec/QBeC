import numpy as np
from qiskit.providers.aer import qasm_simulator
from qiskit import Aer
import matplotlib.pyplot as plt

from QBeC.atom import atom
from QBeC.variable import variable
from QBeC.optimizer import optimizer
from QBeC.ansatz import ansatz
from QBeC.function import ground


Rb = atom(1.44316188e-25, 5.192815e-11)
raxis = variable.oned(-5, 5, 3)

ansatz = ansatz.construct("RealAmplitudes", 4, 3, 'full')

backend = Aer.get_backend('qasm_simulator')
opt = optimizer('SPSA', 5000, ansatz.num_parameters)
num_atoms = [100, 500, 1000, 5000]

dimx = []
dimy = []

for num in num_atoms:
    prob = ground(220, raxis, shots=8192, ansatz=ansatz, backend=backend, num_atoms=num, atom=Rb)
    result = opt.optimize(prob.cost)
    nx , ny = prob.results(result)
    dimx.append(nx)
    dimy.append(ny)


plt.plot(dimx[0], dim[0], label="N=100")
plt.plot(dimx[1], dim[1], label="N=500")
plt.plot(dimx[2], dim[2], label="N=1000")
plt.plot(dimx[3], dim[3], label="N=5000")
plt.show()