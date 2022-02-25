import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, transpile, assemble
from qiskit.circuit.library import TwoLocal, EvolvedOperatorAnsatz, RealAmplitudes
from qiskit.providers.aer import qasm_simulator
from qiskit.algorithms import VQE
from qiskit.algorithms.optimizers import SLSQP, SPSA, ADAM, COBYLA
from qiskit.circuit.library import QFT
from qiskit import Aer
import math
import random
import numpy as np

class ground:
    def __init__(self, trap_freq, raxis, shots, ansatz, backend, num_atoms, atom):
        self.trap_freq = trap_freq
        self.shots = shots
        self.ansatz = ansatz
        self.backend = backend
        self.raxis = raxis
        hbar = 1.0545718e-34
        w = trap_freq
        m = atom.mass
        a1 = np.sqrt(hbar/(m*w))
        a = atom.scatt_length
        N = num_atoms
        self.u = 8*np.pi*a*N/a1
        self.qubits = raxis[2]
        
    def cost(self, x):
        shots = self.shots
        qubits = self.qubits
        backend = self.backend
        ansatz = self.ansatz
        measure = list(range(0, qubits))
        var, varp = self.raxis[0], self.raxis[1]
        qc = QuantumCircuit(qubits,qubits)
        new = ansatz.assign_parameters(x)
        qc.compose(new, inplace=True)
        qc.measure(measure,measure)
        job_sim = backend.run(transpile(qc, backend), shots=shots)
        result_sim = job_sim.result()
        counts = result_sim.get_counts(qc)
        prob = {i: counts[i]/shots for i in counts}
        sum = 0
        for i in prob:
            sum = sum + prob[i]*((var[i])**2)
                
        inter = 0
        for i in prob:
            inter = inter + (prob[i]**2)*self.u*0.5
        pqc = QuantumCircuit(qubits,qubits)
        pnew = ansatz.assign_parameters(x)
        qft = QFT(qubits)
        pqc.compose(pnew, inplace=True)
        pqc.compose(qft, inplace=True)
        pqc.measure(measure,measure)
        job_sim = backend.run(transpile(pqc, backend), shots=shots)
        result_sim1 = job_sim.result()
        counts1 = result_sim1.get_counts(pqc)
        prob1 = {i: counts1[i]/shots for i in counts1}
        psum = 0
        for i in prob1:
            psum = psum + (prob1[i]*((varp[i])**2))
        return (sum+psum+inter)
        
    def results(self, result):
        shots = self.shots
        qubits = self.qubits
        backend = self.backend
        ansatz = self.ansatz
        measure = list(range(0, qubits))
        qc = QuantumCircuit(qubits,qubits)
        new = ansatz.assign_parameters(result)
        qc.compose(new, inplace=True)
        qc.measure(measure,measure)
        job_sim = backend.run(transpile(qc, backend), shots=shots)
        result_sim = job_sim.result()
        counts = result_sim.get_counts(qc)
        prob = {i: counts[i]/shots for i in counts}
        var, varp = self.raxis[0], self.raxis[1]
        
        x = []
        y = []
        for i in prob:
            y.append(prob[i])
            x.append(var[i])
        nx = x.copy()
        nx.sort()
        ny = []
        for i in range (len(nx)):
            for j in range(len(x)):
                if nx[i]==x[j]:
                    ny.append(y[j])
        return nx, ny
            