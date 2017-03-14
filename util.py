from __future__ import division
import numpy as np
import math

class PersonalizedPageRank:
    def __init__(self, vertices, edges=None, adjacencyMatrix=None, alpha=None):
        '''
        vertices should be a list of references to vertex objects (i.e. articles)
        edges should be an nxn numpy matrix (undirected)
        edges_{i, j} is the weight of the edge from i to j 
        '''
        self.vertices = vertices
        if edges is not None:
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

        self.DHalfInverse = np.zeros(shape = D.shape)
        for i in range(self.n):
            self.DHalfInverse[i][i] = math.sqrt(self.DInverse[i][i])
        
        
        #Update transition matrix
        if adjacencyMatrix is not None:
            newTransitionMatrix = self.DInverse*self.transitionMatrix
            self.transitionMatrix = newTransitionMatrix

        #init basis vectors for reference
        self.basisVectors = [0]*self.n
        for i in range(self.n):
            basisI = np.zeros(self.n)
            basisI[i] = 1
            self.basisVectors[i] = basisI

        #init hubvectors 
        self.hubVectors = None
    
    def degree(self, node):
        return self.D[node][node]

    def updateAlpha(self, newAlpha):
        self.computeHubVectors(alpha)
        self.alpha = newAlpha

    def computePPV(self, u, alpha):
        '''
        compute personalized PageRank vector where u is the preference vector
        alpha is the jumping factor
        '''
        if self.hubVectors is None:
            n=self.n
            A = (alpha-1)*self.transitionMatrix + np.identity(n)
            b = alpha*u
            return np.linalg.solve(A, b)
        else:
            weights = [i for i in u]
            ppr = sum([weights[i] * self.hubVectors[i] for i in range(self.n)])
            return ppr

    def computeHubVectors(self, alpha):
        hubVectors = [0]*self.n
        for i in range(self.n):
            basisVec = np.zeros(self.n)
            basisVec[i] = 1
            hubVectors[i] = self.computePPV(basisVec, alpha)
        self.hubVectors = hubVectors

    def getBasisVector(self, i):
        return self.basisVectors[i]
    
    def getHubVector(self, i):
        if not self.hubVectors:
            self.computeHubVectors(self.alpha)
        return self.hubVectors[i]

    def getHubVectors(self):
        if not self.hubVectors:
            self.computeHubVectors(self.alpha)
        return self.hubVectors

    def nodeDistance(self, u, v, alpha):
        ppvu = self.getHubVector(u)
        ppvv = self.getHubVector(v)
        v = ppvu.dot(self.DHalfInverse) + ppvv.dot(self.DHalfInverse)
        return np.linalg.norm(v)

    def distributionDistance(self, p, q, alpha):
        total = 0
        for i in range(self.n):
            for j in range(self.n):
                total += p[i]*q[j]*self.nodeDistance(i, j, alpha)
        return total 
    
    def centerSetEvaluation(C, alpha):
        totalDist = 0
        for i in range(self.n):
            closest = C[0]
            closestDist = float("inf")
            for c in C:
                dist = self.nodeDistance(v, c)
                if dist < closestDist:
                    closestDist = dist
            totalDist += self.degree(i) * closestDist*closestDist
    
    def prVariance(self, alpha):
        total = 0
        for v in range(self.n):
            d = self.degree(v)
            u = self.getHubVector(v)
            b = self.getBasisVector(v)
            dist = self.distributionDistance(b, u, alpha)
            total += d*dist*dist
        return total 
    
    def clusterVariance(self, alpha):
        total = 0
        for v in range(self.n):
            d = self.degree(v)
            #print "make sure hub vecs are initialized for cluster variance"
            stationaryDist = 1/self.n * sum(self.hubVectors)
            u = self.getHubVector(v)
            dist = self.distributionDistance(u, stationaryDist, alpha)
            total += d*dist*dist
        return total



        
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
PPR.nodeDistance(1, 2, .15)
print PPR.prVariance(.15)
print PPR.clusterVariance(.15)


