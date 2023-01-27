from model.models import VoronoiModel
from model.models import DelaunayModel
from preprocessing import PointsGenerater
from display import Displayer
import numpy as np
from table import Table

class Tesselation:

    def __init__(self, points=None):
        self.points = points #生データ
        self.model_points = None #modelが持つpoints, modelインスタンスにデータを持たせる必要がある, またdataを正規化したものが入る
        #Voronoi
        self.v_points_volumes = dict()
        self.v_model = None
        #Delaunay
        self.d_points_volumes = dict()
        self.d_model = None
        #KDE
        self.kde_model = None
        self.kde_density = dict()
        self.kde_function = None

    def voronoi_cal(self, random=False):
        model = VoronoiModel(
            PointsGenerater(self.points).normalization()
        )
        model.cal_volume()
        self.v_model = model
        self.v_points_volumes = model.all_volumes
        self.model_points = model.points

    def v_display(self, dimention, what):
        display = Displayer(dimention)
        if dimention == 2 and any(self.v_points_volumes):
            pass
        elif dimention == 3 and any(self.v_points_volumes):
            if what == 'points':
                display.v_points(self.v_model.points)
            elif what == 'vertices':
                display.points(self.v_model.vertices)
            elif what == 'ridge_points':
                display.v_ridge_points(
                    self.v_model.ridge_points,
                    self.v_model.points
                )
            elif what == 'ridge_vertices':
                display.v_ridge_vertices(
                    self.v_model.ridge_vertices,
                    self.v_model.vertices
                )
            elif what == 'region_points':
                display.v_region_and_points(
                    self.v_model.vertices,
                    self.v_model.regions,
                    self.v_model.point_region
                )
            else:
                pass

    def v_show_data(self):
        table = Table(self.v_model).make_table()
        return table

    def delaunay_cal(self, random=False):
        model = DelaunayModel(
            PointsGenerater(self.points).normalization()
        )
        model.cal_volume()
        self.d_model = model
        self.d_points_volumes = model.all_volumes
        self.model_points = model.points

    def d_display(self, dimention, what):
        display = Displayer(dimention)
        if dimention == 2:
            pass
        elif dimention == 3:
            if what == 'points':
                display.d_points(self.d_model.points)
            elif what == 'region_points':
                display.d_region_and_points(
                    self.d_model.points,
                    self.d_model.vertices
                )

    def d_show_data(self):
        table = Table(self.d_model).make_table()
        return table

    def kernel_density_estimation(self):
        model = KernelDesityEstimation(
            PointsGenerater(self.points).normalization()
        )
        self.kde_density = model.density_estimation()
        self.kde_function = model.kde
        self.kde_model = model
        self.model_points = model.points

    def kde_show_data(self):
        table = Table(self.kde_model).return_table()
        return table

    def kde_delaunay_model_show(self):
        display = Displayer(dimention=2)
        display.kde_d_model_drawing(
            self.model_points,
            self.d_model,
            self.kde_function
        )
