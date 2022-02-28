import numpy as np
from qiskit.providers.aer import qasm_simulator
from qiskit import Aer
import matplotlib.pyplot as plt

from QBeC.atom import atom
from QBeC.variable import variable
from QBeC.optimizer import optimizer
from QBeC.ansatz import ansatz
from QBeC.function import ground


#Creating an instance of atom with it's mass and scattering length
Rb = atom(1.44316188e-25, 5.192815e-11)

#This creates a dictionary with |000...> denoting the starting of axis and |111...> denoting the end as defined
#The space is discretised by 2^num_qubits grid points
raxis = variable.oned(a= -5, b=5, num_qubits=3)

#Define an ansatz here
ansatz = ansatz.construct("RealAmplitudes", reps= 4, num_qubits=3, entanglement='full')

#Defining the backend 
backend = Aer.get_backend('qasm_simulator')

#Defining the optimizer with 5000 iterations
opt = optimizer('SPSA', 5000, ansatz.num_parameters)

#Different number of atoms are taken to check the results
num_atoms = [100, 500, 1000, 5000]

dimx = []
dimy = []

for num in num_atoms:
    #The ground module calculates the ground state wave-function of BEC with 220 as Harmonic Trap frequency
    prob = ground(220, raxis, shots=8192, ansatz=ansatz, backend=backend, num_atoms=num, atom=Rb)
    #Optimizer here minimizes the cost function, which in our case is the energy functional
    result = opt.optimize(prob.cost)
    #nx and ny are the distances in units of harmonic oscillator and probabilty of wave-function respectively
    nx , ny = prob.results(result)
    dimx.append(nx)
    dimy.append(ny)


plt.plot(dimx[0], dimy[0], label="N=100")
plt.plot(dimx[1], dimy[1], label="N=500")
plt.plot(dimx[2], dimy[2], label="N=1000")
plt.plot(dimx[3], dimy[3], label="N=5000")
plt.legend()
plt.show()
