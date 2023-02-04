import numpy as np
import scipy
from scipy import stats

class PointsGenerater:

    def  __init__(self, points):
        self.points = points
        if len(self.points) == 0:
            self.points = self.cone_random_gen()

    def random_generate(self, d, m):
        #n:次元
        #m:個数
        np.random.seed(40)
        self.points = np.random.rand(m, d)
        return self.points

    def two_random_gauss(self):
        np.random.seed(663)
        points_1 = np.random.multivariate_normal(
            [10,10],
            size=(1,300),
            cov=[
                [10,1],
                [0,14]])[0]
        points_2 = np.random.multivariate_normal(
            [-10,-10],
            size=(1,300),
            cov=[
                [15,0],
                [0,20]])[0]
        self.points = np.append(points_1, points_2, axis=0)
        return self.points

    def cone_random_gen(self):
        np.random.seed(800)

        self.points = np.random.multivariate_normal(
            [0,0],
            size=(1,200),
            cov=[
                [50,0],
                [0,50]])[0]

        for i in range(3):
            i += 1
            points_1 = np.random.multivariate_normal(
                [i * 17, i * 17],
                size=(1,200),
                cov=[
                    [50,0],
                    [0,50]])[0]

            points_2 = np.random.multivariate_normal(
                [i * 25, 0],
                size=(1,200),
                cov=[
                    [40,0],
                    [0,50]])[0]
            self.points = np.append(
                np.append(self.points, points_1, axis=0),
                points_2,
                axis=0
            )
        return self.points

    def random_points(self):
        return

    def multiply_lattice_constant(self, points):
        return

    def normalization(self):
        #計算量を下げるため真ん中に寄せる
        return (self.points - np.mean(self.points, axis=0))

class BoxSetter:

    def __init__(self, dimention=3):
        self.dimention = dimention
        self.base_vectors:np.array = np.eyes(dimention)

    def base_vectors_change(self, b_vectors:np.array):
        self.base_vectors = b_vectors
