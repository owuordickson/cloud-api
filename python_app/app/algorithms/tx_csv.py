# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "10 October 2019"

"""
import csv
from datetime import datetime
import numpy as np
import skfuzzy as fuzzy
import multiprocessing as mp
from algorithms.multiprocess import InitParallel
from algorithms.datastream import DataStream


class FuzzTX:
    # allow user to upload multiple csv files

    def __init__(self, file_paths, allow_char, cores, allow_para):
        self.f_paths = FuzzTX.test_paths(file_paths)
        if len(self.f_paths) >= 2:
            if allow_char == 0:
                self.allow_char = False
            else:
                self.allow_char = True

            if cores > 1:
                self.cores = cores
            else:
                self.cores = InitParallel.get_num_cores()

            if allow_para == 0:
                self.allow_parallel = False
            else:
                self.allow_parallel = True

            try:
                self.d_streams = self.get_data_streams()
                self.size = self.get_size()
                self.col_size = 0
                self.boundaries = []
                # self.data_streams, self.time_list = self.get_observations()
                print("data streams fetched")
            except Exception as error:
                raise Exception("CSV Error: "+str(error))
        else:
            raise Exception("Python Error: less than 2 csv files picked")

    def get_size(self):
        size = len(self.d_streams)
        return size

    def get_data_streams(self):
        list_ds = list()
        size = len(self.f_paths)
        for i in range(size):
            path = self.f_paths[i]
            if self.allow_parallel:
                ds = DataStream(i, path, self.allow_char, self.cores)
            else:
                ds = DataStream(i, path, self.allow_char, 0)
            list_ds.append(ds)
        return list_ds

    def cross_data(self):
        print("starting crossing")
        d_streams = self.d_streams
        boundaries, extremes = self.get_boundaries()
        self.boundaries = boundaries

        title_tuple = list()
        # add x_data title tuple
        title_tuple.append("timestamp")  # add title for approximated timestamp
        for ds in d_streams:
            titles = ds.titles
            allowed_cols = ds.allowed_cols
            size = len(titles)
            for i in range(size):
                if i in allowed_cols:
                    title_tuple.append(titles[i])

        self.col_size = len(title_tuple)
        arr_slice = list(np.arange(boundaries[1], extremes[1], extremes[2]))

        if self.allow_parallel:
            # fetch value tuples through parallel processors
            pool = mp.Pool(self.cores)
            x_data = pool.map(self.slide_timestamp, arr_slice)
        else:
            x_data = list()
            for _slice in arr_slice:
                temp_tuple = self.slide_timestamp(_slice)
                x_data.append(temp_tuple)
        x_data = list(filter(bool, x_data))
        x_data.sort()
        x_data.insert(0, title_tuple)

        print("Finished crossing")
        return x_data

    def get_boundaries(self):
        min_time = 0
        max_time = 0
        max_diff = 0
        max_boundary = []
        # list_boundary = list()
        # for item in self.time_list:
        for ds in self.d_streams:
            arr_stamps = ds.timestamps
            min_stamp, max_stamp, min_diff = FuzzTX.get_min_diff(arr_stamps)
            # boundary = [(min_stamp - min_diff), min_stamp, (min_stamp + min_diff)]
            # list_boundary.append(boundary)
            if (max_diff == 0) or (min_diff > max_diff):
                max_diff = min_diff
                max_boundary = [(min_stamp - min_diff), min_stamp, (min_stamp + min_diff)]
            if (min_time == 0) or (min_stamp < min_time):
                min_time = min_stamp
            if (max_time == 0) or (max_stamp > max_time):
                max_time = max_stamp
        extremes = [min_time, max_time, max_diff]
        return max_boundary, extremes

    def slide_timestamp(self, _slice):
        _slice -= self.boundaries[1]  # slice is one step bigger
        new_bounds = [x + _slice for x in self.boundaries]
        boundaries = new_bounds
        arr_index = self.approx_fuzzy_index(boundaries)
        # print(arr_index)
        if arr_index:
            temp_tuple = self.fetch_x_tuples(boundaries[1], arr_index)
            if temp_tuple and len(temp_tuple) == self.col_size:
                return temp_tuple
        return False

    def approx_fuzzy_index(self, boundaries):
        tuple_indices = list()
        # for pop in all_pop:
        for ds in self.d_streams:
            pop = ds.timestamps
            # for each boundary, find times with highest memberships for each dataset
            memberships = fuzzy.membership.trimf(np.array(pop), np.array(boundaries))
            if np.count_nonzero(memberships) > 0:
                index = memberships.argmax()
                var_index = [ds.id, index]
                tuple_indices.append(var_index)
                # tuple_indices.append(index)
                # print(memberships)
            else:
                return False
        return tuple_indices

    def fetch_x_tuples(self, time, arr_index):
        temp_tuple = list()
        temp_tuple.append(str(datetime.fromtimestamp(time)))
        all_ds = self.get_size()
        # for ds in self.d_streams:
        for j in range(all_ds):
            ds = self.d_streams[j]
            for item in arr_index:
                if (ds.id == item[0]) and (item[1] not in ds.fetched_tuples):
                    var_row = ds.data[item[1]]
                    self.d_streams[j].fetched_tuples.append(item[1])
                    size = len(var_row)
                    allowed_cols = ds.allowed_cols
                    for i in range(size):
                        if i in allowed_cols:
                            var_col = var_row[i]
                            temp_tuple.append(var_col)
                    break
        if len(temp_tuple) > 1:
            return temp_tuple
        else:
            return False

    @staticmethod
    def get_min_diff(arr):
        stamps = list(set(arr))
        stamps.sort()
        last = len(stamps) - 1
        min_stamp = stamps[0]
        max_stamp = stamps[last]
        try:
            min_diff = (stamps[1] - stamps[0])
        except IndexError:
            min_diff = 0
        return min_stamp, max_stamp, min_diff

    @staticmethod
    def test_paths(path_str):
        path_list = [x.strip() for x in path_str.split(',')]
        for path in path_list:
            if path == '':
                path_list.remove(path)
        return path_list

    @staticmethod
    def write_csv(csv_data, name='x_data'):
        now = datetime.now()
        stamp = int(datetime.timestamp(now))
        path = name + str(stamp) + str('.csv')
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
            f.close()

    @staticmethod
    def write_file(data, path):
        with open(path, 'w') as f:
            f.write(data)
            f.close()
