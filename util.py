from __future__ import division
import numpy as np

class PersonalizedPageRank:
    def __init__(self, vertices, edges):
        '''
        vertices should be a list of references to vertex objects (i.e. articles)
        edges should be an nxn numpy matrix (undirected)
        edges_{i, j} is the weight of the edge from i to j 
        '''
        self.vertices = vertices
        self.transitionMatrix = edges
        self.hub_vectors = None 

    def computePPV(self, u, alpha):
        '''
        compute personalized PageRank vector where u is the preference vector
        alpha is the jumping factor
        '''
        n=self.transitionMatrix.shape[1]
        A = (alpha-1)*self.transitionMatrix + np.identity(n)
        b = alpha*u
        return np.linalg.solve(A, b)
        
A = np.array([ [0,     0,     0,     1, 0, 1],
            [1/2.0, 0,     0,     0, 0, 0],
            [0,     1/2.0, 0,     0, 0, 0],
            [0,     1/2.0, 1/3.0, 0, 0, 0],
            [0,     0,     1/3.0, 0, 0, 0],
            [1/2.0, 0,     1/3.0, 0, 1, 0 ] ])
u = np.array([[1/6], [1/6], [1/6], [1/6], [1/6], [1/6]])

PPR = PersonalizedPageRank(None, A)
print PPR.computePPV(u, .15)

