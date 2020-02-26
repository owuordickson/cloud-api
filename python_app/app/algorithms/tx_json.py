# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "10 October 2019"
@modified: "26 February 2020"

"""
from multiprocess import InitParallel
from tx_csv import FuzzTX
from datastream_json import DataStream_j


class FuzzTXj(FuzzTX):

    def __init__(self, json_data):
        self.json_data = json_data
        if "datastreams" in json_data:
            self.allow_char = False
            self.cores = InitParallel.get_num_cores()
            self.allow_parallel = True
            try:
                self.d_streams = self.get_data_streams()
                self.size = self.get_size()
                self.col_size = 0
                self.boundaries = []
                print("data streams fetched")
            except Exception as error:
                raise Exception("DS Error: " + str(error))
        else:
            raise Exception("Python Error: dataset has no observations")

    def get_data_streams(self):
        list_ds = list()
        observation_list, time_list = self.get_observations()
        size = len(observation_list)
        for i in range(size):
            ds = DataStream_j(i, observation_list[i], time_list[i], self.allow_char, self.cores)
            list_ds.append(ds)
        return list_ds

    def get_observations(self):
        list_observation = list()
        list_timestamps = list()
        for item in self.json_data["datastreams"]:
            temp_observations = list()
            temp_timestamps = list()
            title = ["timestamp", item["name"]]
            temp_observations.append(title)
            for obj in item["observations"]:
                ok, var_time = DataStream_j.test_time(obj["time"])
                if not ok:
                    return False, False
                # var_temp = [obj["time"], obj["value"]]
                var_temp = [var_time, obj["value"]]
                temp_observations.append(var_temp)
                temp_timestamps.append(var_time)
            list_observation.append(temp_observations)
            list_timestamps.append(temp_timestamps)
        return list_observation, list_timestamps
