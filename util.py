from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
import math
import misc


class PersonalizedPageRank:
    def __init__(self, edges=None, adjacencyMatrix=None, alpha=None):
        '''
        vertices should be a list of references to vertex objects (i.e. articles)
        edges should be an nxn numpy matrix (undirected)
        edges_{i, j} is the weight of the edge from i to j 
        '''
        if edges is not None:
            self.transitionMatrix = edges
        else:
            self.transitionMatrix = adjacencyMatrix #temporarily
        self.hub_vectors = None 
        self.n = self.transitionMatrix.shape[1]
        self.alpha = alpha
        if not alpha:
            self.alpha = .15
        
        #Initialize degree matrix
        degrees = [0]*self.n
        for i in range(self.n):
            degrees[i] = np.count_nonzero(self.transitionMatrix[i])

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
            newTransitionMatrix = self.DInverse.dot(self.transitionMatrix)
            self.transitionMatrix = newTransitionMatrix

        self.basisVectors = [0]*self.n
        for i in range(self.n):
            basisI = np.zeros(self.n)
            basisI[i] = 1
            self.basisVectors[i] = basisI

        #init hubvectors 
        self.hubVectors = None

        #print self.transitionMatrix
        #print self.D
        #print self.DInverse
    
    def degree(self, node):
        return self.D[node][node]

    def updateAlpha(self, newAlpha):
        self.computeHubVectors(newAlpha)
        self.alpha = newAlpha

    def pageRank(self):
        vals, vecs = np.linalg.eig(self.transitionMatrix.T)
        v = vecs[:,0]
        v *= 1/sum(v)
        return v

    def computePPV(self, u, alpha):
        '''
        compute personalized PageRank vector where u is the preference vector
        alpha is the jumping factor
        '''
        if self.hubVectors is None or alpha != self.alpha:
            n=self.n
            A = (alpha-1)*self.transitionMatrix.T + np.identity(n)
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
    
    def centerSetEvaluation(self, C, alpha):
        totalDist = 0
        for i in range(self.n):
            closest = None
            closestDist = float("inf")
            for c in C:
                dist = self.nodeDistance(i, c, alpha)
                if dist < closestDist:
                    closestDist = dist
            totalDist += self.degree(i) * closestDist*closestDist
        return totalDist
    
    def prVariance(self, alpha):
        total = 0
        if alpha != self.alpha:
            self.updateAlpha(alpha)
        for v in range(self.n):
            d = self.degree(v)
            u = self.getHubVector(v)
            b = self.getBasisVector(v)
            dist = self.distributionDistance(b, u, alpha)
            total += d*dist*dist
            #print 'variance at', alpha, 'is', total
        return total 
    
    def clusterVariance(self, alpha):
        total = 0
        if alpha != self.alpha:
            self.updateAlpha(alpha)
        for v in range(self.n):
            d = self.degree(v)
            #print "make sure hub vecs are initialized for cluster variance"
            stationaryDist = 1/self.n * sum(self.hubVectors)
            u = self.getHubVector(v)
            dist = self.distributionDistance(u, stationaryDist, alpha)
            total += d*dist*dist
        return total

    def volume(self, T):
        vol = 0
        for v in T:
            vol += self.degree(v)
        return vol

    def assignVerticesToCenters(self, C, alpha):
        assignment = {c:list() for c in C}
        for v in range(self.n):
            bestDist = float("inf")
            closestNode = C[0]
            for c in C:
                if self.nodeDistance(v, c, alpha) < bestDist:
                    bestDist = self.nodeDistance(v, c, alpha)
                    closestNode = c
            assignment[closestNode].append(v)
        return assignment

    def setClusterVariance(self, C, alpha):
        if alpha != self.alpha:
            self.updateAlpha(alpha)
        total = 0
        assignment = self.assignVerticesToCenters(C, alpha)
        for c in C:
            vol = self.volume(assignment[c])
            stationaryDist = 1/self.n * sum(self.getHubVectors())
            dist = self.distributionDistance(self.getBasisVector(c), stationaryDist, alpha)
            total += vol * dist * dist
        return total
        
        
   
if __name__ == '__main__':
    a = '0, 1, 0, 1, 0, 1'
    b = '1, 0, 1, 0, 1, 0'
    c = '0, 1, 0, 0, 0, 0'
    d = '1, 0, 0, 0, 0, 1'
    e = '0, 1, 0, 0, 0, 0'
    f = '1, 0, 0, 1, 0, 0'
    E = np.matrix('%s;%s;%s;%s;%s;%s' % (a, b, c, d, e, f))
    u = [1/6]*6
    u = np.matrix(u)
    degree = [3, 3, 1, 2, 1, 2]
    D = np.zeros(shape=(6, 6))
    for i in range(6):
        D[i][i] = 1/degree[i]

    PPR = PersonalizedPageRank(adjacencyMatrix = E)
    PPR.computeHubVectors(.1)
    v = [PPR.prVariance(alpha) for alpha in np.arange(0, 1, .01)]
    #plt.plot(np.arange(0, 1, .01), v)
    #plt.show()
    print PPR.setClusterVariance([1, 2, 3], .15)
    print PPR.centerSetEvaluation([1, 2, 3], .1)
    print PPR.setClusterVariance([1, 2, 3], .1)
    print PPR.clusterVariance(.1)
    print PPR.prVariance(.1)
