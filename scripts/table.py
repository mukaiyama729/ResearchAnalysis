import pandas as pd
from scipy.spatial import ConvexHull


class Table:
    def __init__(self, model):
        self.model = model
        self.model_name = model.name
        self.points = model.points
        self.volumes = model.all_volumes
        self.vertices = model.vertices
        self.CHes = model.all_CHes
        self.table = None

    def make_table(self):
        if self.model_name == 'Delaunay':
            num_of_simplices = len(self.model.simplices)
            self.table = pd.DataFrame(
                index=[i for i in range(num_of_simplices)],
                columns=[
                    'volume',
                    'vertices',
                    'num_of_vertices',
                    'convex_hull_index'
                    ]
            )
            for i in range(num_of_simplices):
                self.table.iloc[i,:] = [
                    self.volumes[i],
                    tuple(self.points[self.vertices[i]]),
                    tuple(self.vertices[i]),
                    i
                ]
            return self.table
        elif self.model_name == 'Voronoi':
            self.table = pd.DataFrame(
                columns=['volume',
                        'vertices',
                        'num_of_vertices',
                        'convex_hull_index(index_of_point)'
                        ],
                index=[i for i in range(len(self.model.cleaned_points))]
            )
            counter = 0
            for i in self.model.cleaned_points:
                self.table.iloc[counter,:] = [
                    self.volumes[i],
                    self.vertices[self.model.regions[self.model.point_region[i]]],
                    self.model.regions[self.model.point_region[i]],
                    i
                ]
                counter += 1
            return self.table
