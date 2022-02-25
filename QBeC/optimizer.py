from qiskit.algorithms.optimizers import SLSQP, SPSA, ADAM, COBYLA
import numpy as np
class optimizer:
    def __init__(self, name, iterations, num_parameters):
        self.name = name
        self.iterations = iterations
        self.num_parameters = num_parameters
        

        
        self.initial_point = np.random.random(self.num_parameters)
    def optimize(self, loss):
        if self.name == 'SPSA':
            opt = SPSA(maxiter=self.iterations)
        result = opt.optimize(self.num_parameters, loss, initial_point=self.initial_point)
        return result[0]