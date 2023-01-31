import pandas as pd
from scipy.spatial import ConvexHull
import numpy as np


class Table:

    def __init__(self, model):
        self.model = model
        self.model_name = model.name
        self.points = model.points
        self.v_table = pd.DataFrame()
        self.d_table = pd.DataFrame()
        self.kde_table = pd.DataFrame()

    def make_table(self):
        if self.model_name == 'Delaunay':
            num_of_points = len(self.model.points)
            self.d_table = pd.DataFrame(
                index=[i for i in range(num_of_points)],
                columns=[
                    'volume',
                    'point_index'
                    ]
            )
            for i in range(num_of_points):
                self.d_table.iloc[i,:] = [
                    self.model.point_volume_dict[i],
                    i
                ]
            self.d_table = self.d_table.apply(pd.to_numeric)
            return self.d_table

        elif self.model_name == 'Voronoi':
            self.v_table = pd.DataFrame(
                columns=['volume',
                        'vertices',
                        'num_of_vertices',
                        'convex_hull_index(index_of_point)'
                        ],
                index=[i for i in range(len(self.model.cleaned_points))]
            )
            counter = 0
            for i in self.model.cleaned_points:
                self.v_table.iloc[counter,:] = [
                    self.model.all_volumes[i],
                    self.model.vertices[self.model.regions[self.model.point_region[i]]],
                    self.model.regions[self.model.point_region[i]],
                    i
                ]
                counter += 1
            self.v_table[['volume', 'convex_hull_index(index_of_point)']] = self.v_table[['volume', 'convex_hull_index(index_of_point)']].apply(pd.to_numeric)
            return self.v_table

        elif self.model_name == 'KDE':
            self.kde_table = pd.DataFrame(
                columns=['density', 'point_index', 'point'],
                index=[i for i in range(len(self.model.points))]
            )
            for index, density in self.model.density_dict.items():
                self.kde_table.iloc[index,:] = [
                    density,
                    index,
                    self.model.points[index]
                ]
            self.kde_table[['density', 'point_index']] = self.kde_table[['density', 'point_index']].apply(pd.to_numeric)
            return self.kde_table

    def is_table(self):
        if self.model_name == 'Delaunay':
            return bool(any(self.d_table))
        elif self.model_name == 'Voronoi':
            return bool(any(self.v_table))
        elif self.model_name == 'KDE':
            return bool(any(self.kde_table))

    def return_table(self):
        if self.model_name == 'Delaunay':
            if self.is_table():
                return self.d_table
            else:
                return self.make_table()
        elif self.model_name == 'Voronoi':
            if self.is_table():
                return self.v_table
            else:
                return self.make_table()
        elif self.model_name == 'KDE':
            if self.is_table():
                return self.kde_table
            else:
                return self.make_table()

    @staticmethod
    def take_higher(p_v_dict, per):
        higher = np.percentile(np.array(list(p_v_dict.values())), per)
        return dict(filter(lambda item: item[1] > higher, p_v_dict.items()))
