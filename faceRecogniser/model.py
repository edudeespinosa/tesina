import numpy as np
from faceRecogniser.facerecutil import asRowMatrix
from faceRecogniser.facerecutil import asColumnMatrix
from faceRecogniser.facerecutil import EuclideanDistance
from faceRecogniser.pca import pca, project


class EigenfacesModel (object):

    def __init__(self, X=None, y=None, dist_metric=EuclideanDistance(), num_components=0):
        self.dist_metric = dist_metric
        self.num_components = 0
        self.projections = []
        self .W = []
        self.mu = []
        # if (X is not None ) and (y is not None ):
        #     self.compute (X ,y)

    def compute(self, X, y):
        [D, self.W, self.mu] = pca(asRowMatrix(X), y, self.num_components)
        # store labels
        self.y = y
        # store projections
        for xi in X:
            self.projections.append(
                project(self .W, xi.reshape(1, -1), self.mu))
        return [D, self.W, self.mu]

    def predict(self, X):
        minDist = np.finfo('float').max
        minClass = -1
        Q = project(self .W, X. reshape(1, -1), self.mu)
        for i in xrange(len(self.projections)):
            dist = self.dist_metric(self.projections[i], Q)
            if dist < minDist:
                minDist = dist
                minClass = self.y[i]
        return minClass
