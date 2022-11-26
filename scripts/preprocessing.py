import numpy as np
import scipy
from scipy import stats

class PointsGenerater:

    def  __init__(self, points:np.array=None):
        self.points:np.array = points
        if not points:
            self.points = self.random_generate(3,100)

    def random_generate(self, d, m):
        #n:次元
        #m:個数
        np.random.seed(6)
        self.points = np.random.rand(m, d)
        return self.points

    def random_points(self):
        return

    def multiply_lattice_constant(self, points):
        return

    def normalization(self):
        return stats.stats.zscore(self.points)

class BoxSetter:

    def __init__(self, dimention=3):
        self.dimention = dimention
        self.base_vectors:np.array = np.eyes(dimention)

    def base_vectors_change(self, b_vectors:np.array):
        self.base_vectors = b_vectors
