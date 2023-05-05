import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as la

class Circuit:
    def __init__(self, netlist):
        self.netlist = netlist
        self.nnodes = len(self.netlist.getKeys())
        self.node_map = dict(zip(self.netlist.getKeys(), range(self.nnodes)))
        
        # Constructing the MNA matrices
        self.G = sp.lil_matrix((self.nnodes, self.nnodes))
        self.B = sp.lil_matrix((self.nnodes, 1))
        self.C = sp.lil_matrix((self.nnodes, self.nnodes))
        self.D = sp.lil_matrix((self.nnodes, 1))
        
        # Fill G, B, C, and D matrices using netlist
        for key in self.netlist.getKeys():
            for element in self.netlist.get(key):
                n1 = self.node_map[element.n1]
                n2 = self.node_map[element.n2]
                value = element.value
                
                if isinstance(element, Resistor):
                    g = 1.0 / value
                    self.G[n1, n1] += g
                    self.G[n2, n2] += g
                    self.G[n1, n2] -= g
                    self.G[n2, n1] -= g
                elif isinstance(element, VoltageSource):
                    self.B[n1, 0] -= value
                    self.B[n2, 0] += value
                    self.C[n1, n2] += 1.0
                    self.C[n2, n1] -= 1.0
                elif isinstance(element, CurrentSource):
                    self.D[n1, 0] -= value
                    self.D[n2, 0] += value

    def solve(self):
        A = sp.vstack([sp.hstack([self.G, self.C]), sp.hstack([self.B, self.D])])
        b = np.zeros((2*self.nnodes, 1))
        b[self.nnodes:, 0] = -1.0
        x = la.spsolve(A, b)
        
        # Print out the node voltages
        for key in self.netlist.getKeys():
            node = self.node_map[key]
            voltage = x[node, 0]
            print("Node {}: {:.4f} V".format(key, voltage))
