import glob
import os
import pathlib
import re
import os
import tqdm
import numpy as np
import pandas as pd
class FileLoader:

    @classmethod
    def generate_data(cls, data_path):
        data = []
        with open(data_path, 'r') as f:
            read_line = f.readlines()

        name_info_list = list(
            map(float, cls.extract_file_name_info(os.path.basename(data_path)))
            )

        for line in read_line[25:]:
            record_list = list(map(float, line.replace('\n', '').replace(' ', '').split('\t')))
            record_list.extend(name_info_list)
            data.append(record_list)

        return data

    @staticmethod
    def list_of_files(directory_path, suffix):
        files = glob.glob(os.path.join(directory_path, '*'+ suffix))
        return files

    @classmethod
    def construct_data(cls, directory_path, suffix='.txt'):
        data = []

        for path in FileLoader.list_of_files(directory_path, suffix):
            data.extend(cls.generate_data(path))

        return np.array(data)

    def to_float(self, record_list):
        float_list = []
        for num in record_list:
            float_list.append(float(num))
        return float_list

    @classmethod
    def extract_file_name_info(cls, file_name):
        return re.findall(r'\d+', file_name)

class Saver:

    @staticmethod
    def pd_to_csv(df, path):
        pass
