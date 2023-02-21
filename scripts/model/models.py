import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, Delaunay, ConvexHull
import random
import scipy
from scipy import stats
import tqdm
from scipy.stats import gaussian_kde
from sklearn import neighbors

class VoronoiModel:

    def __init__(self, points:np.array ):

        '''
            #[[1,2,3,4],[71,3,21,4],[-1,3,42,4]...]それぞれはveriticesのインデックス
            self.regions = self.vor.regions

            #keyがpointのインデックスでvalueがregionのインデックス
            self.point_region = self.vor.point_region
            #以下いずれも、立体を作れないもののデータは除いてある
            #-1をregionsに含むものをのぞいている

            #keyはpointsのインデックス,valueはConvexHullオブジェクト
            self.all_CHes = dict()
            #keyはpointsのインデックス,valueはその体積
            self.all_volumes = dict()

            self.cleaned_points = list()
        '''

        self.vor = Voronoi(points)
        self.points = self.vor.points
        self.vertices = self.vor.vertices
        self.ridge_vertices = self.vor.ridge_vertices
        self.ridge_points = self.vor.ridge_points
        self.regions = self.vor.regions
        self.point_region = self.vor.point_region
        self.all_volumes = dict()
        self.all_CHes = dict()
        self.cleaned_points = list()
        self.name = 'Voronoi'

    def cal_volume(self):
        num_of_points = len(self.points)

        for i in tqdm.tqdm(range(num_of_points)):
            region = self.regions[self.point_region[i]]
            if -1 in tuple(region):
                ch = ConvexHull(self.vertices[region])
                self.all_volumes[i], self.all_CHes[i] = 0, ch
                self.cleaned_points.append(i)
                continue
            ch = ConvexHull(self.vertices[region])
            self.all_volumes[i], self.all_CHes[i] = ch.volume, ch
            self.cleaned_points.append(i)

    def remove_edge_points():
        return

class DelaunayModel:

    def __init__(self, points:np.array):

        '''
            #点のベクトルのリスト[[0.1,4.5,6.3],[2,4.9,7.1]...]インデックスが点の番号
            self.points = self.dln.points
            #三角系をなしている点のリストのリスト[[1,3,2,1],[1,0,4,2]...]
            self.vertices = self.dln.vertices
            #三角系をなしている点のリストのリスト[[1,3,2,5],[1,0,4,2]...]
            self.simplices = self.dln.simplices
            # 凸包の底面のリスト[[1,2,0],[3,4,5]...]
            self.convex_hull = self.dln.convex_hull
            #simplicesのインデックス,key三角形のインデックス(simplicesのいんでくす),value:その三角形のConvexHullオブジェクト
            self.all_CHes = self._return_CHes()
            #convexの体積の辞書key:三角形のインデックる,value:その三角形の体積
            self.all_volumes = dict()
            #あるpointのnum(key)に足してそれが属する三角形の体積のリスト(value)、上から番号を付与している
            self.dict_of_points_and_volumes
            #あるpointのnum(key)にたいしてそれが属する三角形の体積全ての平均値(value)
            self.point_volume_dict
            self.name = 'Delaunay'
        '''

        self.dln = Delaunay(points)
        self.points = self.dln.points
        self.vertices = self.dln.vertices
        self.simplices = self.dln.simplices
        self.convex_hull = self.dln.convex_hull
        self.all_CHes = self._return_CHes()
        self.all_volumes = dict()
        self.dict_of_points_and_volumes = self.make_empty_dict()
        self.point_volume_dict = dict()
        self.name = 'Delaunay'

    def _return_CHes(self):
        print('ch')
        regions = dict()
        ch = ConvexHull
        for i, j in tqdm.tqdm(enumerate(self.simplices)):
            regions[i] = ch(
                self.points[j]
            )
        return regions

    def cal_volume(self):
        print('volume_cal')
        num_of_simplices = len(self.simplices)
        for i in tqdm.tqdm(range(num_of_simplices)):
            self.all_volumes[i] = self.all_CHes[i].volume
        self.cal_point_volume()

    def cal_point_volume(self):

        print('cal_point_volume')
        for volume_num, ver in tqdm.tqdm(enumerate(self.vertices)):
            for point_num in ver:
                self.dict_of_points_and_volumes[point_num].append(self.all_volumes[volume_num])

        for num ,value in tqdm.tqdm(self.dict_of_points_and_volumes.items()):
            how_many = len(value)
            try:
                self.point_volume_dict[num] = sum(value) / how_many
            except ZeroDivisionError:
                self.point_volume_dict[num] = 0

    def make_empty_dict(self):
        print('emtpy_dict')
        dict_of_points_and_volumes = dict()
        for i in tqdm.tqdm(range(len(self.points))):
            dict_of_points_and_volumes[i] = []
        return dict_of_points_and_volumes



class KernelDesityEstimation:

    '''
    kernel関数数はガウスカーネル
    三角形や四角形のカーネルの方が良さそう
    いつか実装する
    '''

    def __init__(self, points:np.array):
        self.points = points
        self.transposed_points = points.T
        self.density_dict = dict()
        self.kde = None
        self.name = 'KDE'

    def density_estimation(self, alg='none', model='gaussian'):
        if alg == 'none':
            self.kde = gaussian_kde(self.transposed_points)
            for num, point in tqdm.tqdm(enumerate(self.points)):
                self.density_dict[num] = self.kde.evaluate(point)[0]
            return self.density_dict
        elif alg == 'kd_tree' or alg == 'ball_tree':
            self.kde = neighbors.KernelDensity(
                kernel=model,
                algorithm=alg,
                bandwidth='silverman',
                ).fit(self.points)

            indices = [index for index in range(len(self.points))]
            self.density_dict = dict(zip(indices, list(np.exp(self.kde.score_samples(self.points)))))
            return self.density_dict


