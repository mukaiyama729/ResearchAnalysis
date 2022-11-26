from model.models import VoronoiModel
from preprocessing import PointsGenerater
from display import Displayer
import numpy as np

class Tessellation:

    def __init__(self, points:np.array=None):
        self.points = points
        self.v_points_volumes = dict()
        self.v_model = None
        self.d_points_volumes = dict()
        self.d_model = None

    def voronoi_cal(self, random=False):
        model = VoronoiModel(
            PointsGenerater(self.points).normalization()
        )
        model.cal_volume()
        self.v_model = model
        self.v_points_volumes = model.all_volumes

    def v_display(self, dimention:int, what):
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
