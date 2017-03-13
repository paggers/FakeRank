from __future__ import division
import numpy as np

class PersonalizedPageRank:
    def __init__(self, vertices, edges=None, adjacencyMatrix=None, alpha=None):
        '''
        vertices should be a list of references to vertex objects (i.e. articles)
        edges should be an nxn numpy matrix (undirected)
        edges_{i, j} is the weight of the edge from i to j 
        '''
        self.vertices = vertices
        if edges:
            self.transitionMatrix = edges
        else:
            self.transitionMatrix = adjacencyMatrix #temporarily
        self.hub_vectors = None 
        self.n = edges.shape[1]
        self.alpha = alpha
        if not alpha:
            self.alpha = .15
        
        #Initialize degree matrix
        degrees = [0]*self.n
        for i in range(self.n):
            for entry in self.transitionMatrix[i]:
                if entry != 0:
                    degrees[i] += 1
        D=np.zeros(shape=(self.n, self.n))
        for i in range(self.n):
            D[i][i] = degrees[i]
        self.D = D

        #initialize inverse D matrix
        self.DInverse = np.zeros(shape = D.shape)
        for i in range(self.n):
            self.DInverse[i][i] = 1/degrees[i]
        print self.DInverse
        print self.D
        
        if adjacencyMatrix:
            newTransitionMatrix = self.DInverse*self.transitionMatrix
            self.transitionMatrix = newTransitionMatrix
                    

    def computePPV(self, u, alpha):
        '''
        compute personalized PageRank vector where u is the preference vector
        alpha is the jumping factor
        '''
        n=self.transitionMatrix.shape[1]
        A = (alpha-1)*self.transitionMatrix + np.identity(n)
        b = alpha*u
        return np.linalg.solve(A, b)

    def computeHubVectors(self, alpha):
        hubVectors = [0]*self.n
        for i in range(self.n):
            basisVec = np.zeros(self.n)
            basisVec[i] = 1
            hubVectors[i] = self.computePPV(basisVec, alpha)
        self.hubVectors = hubVectors
    
    def getHubVector(self, i):
        if not self.hubVectors:
            self.computeHubVectors(self.alpha)
        return self.hubVectors[i]

    def getHubVectors(self):
        if not self.hubVectors:
            self.computeHubVectors(self.alpha)
        return self.hubVectors
    
    #def distance(self, u, v, alpha):



        
A = np.array([ [0,     0,     0,     1, 0, 1],
            [1/2.0, 0,     0,     0, 0, 0],
            [0,     1/2.0, 0,     0, 0, 0],
            [0,     1/2.0, 1/3.0, 0, 0, 0],
            [0,     0,     1/3.0, 0, 0, 0],
            [1/2.0, 0,     1/3.0, 0, 1, 0 ] ])
u = np.ones(6)
u*= (1/6)

PPR = PersonalizedPageRank(None, A)
PPR.computeHubVectors(.15)
vectors = PPR.getHubVectors()
average = 0
for vector in vectors:
    average += vector
average = average * (1/PPR.n)
print average
print PPR.computePPV(u, .15)

