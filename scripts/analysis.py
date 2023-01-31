import glob
import os
import pathlib
import re
import os
import tqdm
import numpy as np
import pandas as pd
from .tessellation import Tessellation
from .load_file import FileLoader
from .arrange_data import ArrangeData

class Analyzer(Tessellation):

    def __init__(self, directory_path):
        self.data = pd.DataFrame(FileLoader.construct_data(directory_path), columns=['time', 'x', 'y', 'z', 'trial', 'cycle', 'reprica'])
        self.points = np.array(self.data.loc[:, ['x', 'y', 'z']], dtype='float')
        super().__init__(self.points)
        self.d_result = None
        self.v_result = None
        self.kde_result = None

    def show_data_delaunay(self):
        calculated_table = self.d_show_data()
        merged_table = pd.merge(self.data, calculated_table, how='outer', left_index=True, right_index=True)
        self.d_result = merged_table
        return merged_table

    def show_data_kde(self):
        calculated_table = self.kde_show_data()
        merged_table = pd.merge(self.data, calculated_table, how='outer', left_index=True, right_index=True)
        self.kde_result = merged_table
        return merged_table

    def show_data_voronoi(self):
        calculated_table = self.v_show_data()
        merged_table = pd.merge(self.data, calculated_table, how='outer', left_index=True, right_index=True)
        self.v_result = merged_table
        return merged_table

    def high_volume_d_point(self, percent=10):
        self.arranger = ArrangeData(self.d_result)
        return self.arranger.sorted_points_of_high_volume(percent)

    def high_volume_d_trajectories(self):
        self.arranger = ArrangeData(self.d_result)
        return self.arranger.averaged_trajectory_data()

    def is_model(self):
        pass


