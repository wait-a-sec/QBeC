from qiskit.circuit.library import TwoLocal, EvolvedOperatorAnsatz, RealAmplitudes

class ansatz:
    def __init__(self):
        pass
        
    def construct(name, reps, num_qubits, entanglement):
        if name == 'RealAmplitudes':
            temp = RealAmplitudes(num_qubits = num_qubits, entanglement=entanglement, reps=reps)
    
        if name == 'TwoLocal':
            temp = TwoLocal(num_qubits = num_qubits,rotation_blocks=['ry', 'rz'], entanglement_blocks=['cz'], entanglement=entanglement, reps=reps)
        
        return temp