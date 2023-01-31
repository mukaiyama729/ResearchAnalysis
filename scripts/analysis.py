import glob
import os
import pathlib
import re
import os
import tqdm
import numpy as np
import pandas as pd
from .tessellation import Tessellation

class Analyzer(Tessellation):

    def __init__(self, directory_path):
        self.data = pd.DataFrame(self.construct_data(directory_path), columns=['time', 'x', 'y', 'z', 'trial', 'cycle', 'reprica'])
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

    def generate_data(self, data_path):
        data = []
        with open(data_path, 'r') as f:
            read_line = f.readlines()

        name_info_list = self.extract_file_name_info(
            os.path.basename(data_path)
        )

        for line in read_line[25:]:
            record_list = list(map(float, line.replace('\n', '').replace(' ', '').split('\t')))
            record_list.extend(name_info_list)
            data.append(record_list)

        return data

    def list_of_files(self, directory_path, suffix):
        files = glob.glob(os.path.join(directory_path, '*'+ suffix))
        return files

    def construct_data(self, directory_path, suffix='.txt'):
        data = []

        for path in self.list_of_files(directory_path, suffix):
            data.extend(self.generate_data(path))

        return np.array(data)

    def to_float(self, record_list):
        float_list = []
        for num in record_list:
            float_list.append(float(num))
        return float_list

    def extract_file_name_info(self, file_name):
        return re.findall(r'\d+', file_name)


