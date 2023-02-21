import glob
import os
import pathlib
import re
import os
import tqdm
import numpy as np
import pandas as pd
import pickle
from .tessellation import Tessellation
from .load_file import FileLoader
from .arrange_data import ArrangeData
import time


class Analyzer(Tessellation):

    def __init__(self):
        self.points = None
        self.d_result = None
        self.v_result = None
        self.kde_result = None

    def load_file(self, directory_path):
        self.data = pd.DataFrame(FileLoader.construct_data(directory_path), columns=['time', 'x', 'y', 'z', 'trial', 'cycle', 'reprica'])
        self.points = np.array(self.data.loc[:, ['x', 'y', 'z']], dtype='float')
        super().__init__(self.points)

    def load_array(self, arr):
        self.points = arr
        super().__init__(self.points)

    def create_delaunay_data(self):
        self.delaunay_cal()
        calculated_table = self.d_show_data()
        merged_table = pd.merge(self.data, calculated_table, how='outer', left_index=True, right_index=True)
        self.d_result = merged_table

    def create_kde_data(self, kernel='gaussiann'):
        self.kernel_density_estimation(kernel=kernel)
        calculated_table = self.kde_show_data()
        merged_table = pd.merge(self.data, calculated_table, how='outer', left_index=True, right_index=True)
        self.kde_result = merged_table

    def create_voronoi_data(self):
        self.voronoi_cal()
        calculated_table = self.v_show_data()
        print('a')
        merged_table = pd.merge(self.data, calculated_table, how='outer', left_index=True, right_index=True)
        self.v_result = merged_table

    def large_volume_d_point(self, percent=10):
        self.arranger = ArrangeData(self.d_result)
        return self.arranger.sorted_points_of_large_volume(percent)

    def large_volume_v_point(self, percent=10):
        self.arranger = ArrangeData(self.v_result)
        return self.arranger.sorted_points_of_large_volume(percent)

    def low_density_kde_point(self, percent=10):
        self.arranger = ArrangeData(self.kde_result)
        return self.arranger.sorted_points_of_low_density(percent)

    def meaned_trajectory(self, model_name):
        try:
            if model_name == 'delaunay':
                self.arranger = ArrangeData(self.d_result)
                return self.arranger.averaged_trajectory_data().sort_values('volume', ascending=False)
            elif model_name == 'voronoi':
                self.arranger = ArrangeData(self.v_result)
                return self.arranger.averaged_trajectory_data().sort_values('volume', ascending=False)
            elif model_name == 'kde':
                self.arranger = ArrangeData(self.v_result)
                return self.arranger.averaged_trajectory_data().sort_values('density')
            else:
                print('delaunay, voronoi or kde are model_name.')
                pass
        except:
            print('Please make a data using model.')

    def is_model(self):
        pass

    def save_instance(self, directory_path, file_name):
        with open(directory_path + file_name, 'wb') as f:
            pickle.dump(self, f)

    def save_data(self, df, directory_path, file_name):
        df.to_csv(directory_path + file_name)

    def calculate_all_model(self):
        print('d')
        s = time.time()
        self.create_delaunay_data()
        print(time.time() - s)
        print('v')
        s = time.time()
        self.create_voronoi_data()
        print(time.time() - s)
        print('kde')
        s = time.time()
        self.create_kde_data(kernel='epanechnikov')
        print(time.time() - s)

    def save_all_data(self, directory_path, instance_file_name, d_file_name, v_file_name, kde_file_name, data_file_name):
        self.calculate_all_model()
        self.save_instance(directory_path, instance_file_name)
        self.save_data(self.d_result, directory_path, d_file_name)
        self.save_data(self.v_result, directory_path, v_file_name)
        self.save_data(self.kde_result, directory_path, kde_file_name)
        self.save_data(self.data, directory_path, data_file_name)


