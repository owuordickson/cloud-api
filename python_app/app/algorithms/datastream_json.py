# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "26 February 2020"

"""

from algorithms.datastream import DataStream


class DataStream_j(DataStream):

    def __init__(self, _id, raw_ds, t_stamps, allow_char, cores):
        self.id = _id
        self.path = raw_ds[1][1]
        self.allow_char = allow_char
        self.cores = cores
        self.raw_data = raw_ds
        if len(self.raw_data) == 0:
            print("csv file read error")
            raise Exception("Unable to read csv file: " + self.path)
        else:
            self.data = self.raw_data
            self.titles = self.get_titles()
            self.time_col = 0
            self.allowed_cols =[1]
            self.timestamps = t_stamps
            self.fetched_tuples = list()
