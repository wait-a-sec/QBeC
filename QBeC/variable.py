import numpy as np

class variable:
    def __init__(self):
        pass
    def oned(a, b, num_qubits):
        h = (b-a)/(2**num_qubits)
        varx = {}
        varp = {}
        char = "0"+str(num_qubits)+"b"
        for i in range(2**num_qubits):
            varx[format(i, char)] = a+i*h
            if i< int((2**num_qubits)/2):
                varp[format(i, char)] = (2*np.pi*i)/(b-a)
            else:
                varp[format(i, char)] = -(2*np.pi*(2**num_qubits-i))/(b-a)
        return [varx, varp, num_qubits]