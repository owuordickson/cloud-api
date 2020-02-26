# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "09 December 2019"

"""
import csv
import time
import multiprocessing as mp
from dateutil.parser import parse


class DataStream:

    def __init__(self, _id, path, allow_char, cores):
        self.id = _id
        self.path = path
        self.allow_char = allow_char
        self.cores = cores
        self.raw_data = DataStream.read_csv(path)
        if len(self.raw_data) == 0:
            print("csv file read error")
            raise Exception("Unable to read csv file: " + path)
        else:
            self.data = self.raw_data
            self.titles = self.get_titles()
            self.time_col = False
            self.allowed_cols, self.timestamps = self.init_ds()
            self.fetched_tuples = list()

    def get_titles(self):
        data = self.raw_data
        if data[0][0].replace('.', '', 1).isdigit() or data[0][0].isdigit():
            return False
        else:
            if data[0][1].replace('.', '', 1).isdigit() or data[0][1].isdigit():
                return False
            else:
                titles = []
                for i in range(len(data[0])):
                    # sub = [str(i+1), data[0][i]]
                    sub = str(data[0][i])
                    titles.append(sub)
                del self.data[0]
                return titles

    def init_ds(self):
        data = self.data
        # test for time from any row
        t_index, allowed_cols = self.test_ds_data(data[1])
        if t_index is None:
            raise Exception("No time found in file: " + str(self.path))
            # return False
        else:
            self.time_col = t_index
            if self.cores > 0:
                # fetch timestamp from every row through parallel processors
                size = len(data)
                tasks = range(size)
                pool = mp.Pool(self.cores)
                timestamps = pool.map(self.get_time_stamp, tasks)
            else:
                timestamps = list()
                size = len(data)
                for i in range(size):
                    t_stamp = self.get_time_stamp(i)
                    timestamps.append(t_stamp)
            timestamps.sort()
            allowed_cols.sort()
            print("Finished fetching timestamps")
        return allowed_cols, timestamps

    def get_time_stamp(self, i):
        # print("fetching time stamp")
        row = self.data[i]
        t_value = row[self.time_col]
        time_ok, t_stamp = DataStream.test_time(t_value)
        if time_ok:
            return t_stamp
        else:
            raise Exception(str(t_value) + ' : time is invalid for ' + str(self.path))

    def test_ds_data(self, row):
        print("testing data stream data")
        time_index = None
        allowed_cols = list()
        size = len(row)
        for col_index in range(size):
            col_value = row[col_index]
            time_ok, t_stamp = DataStream.test_time(col_value)
            if time_ok:
                # return col_index, t_stamp
                if time_index is None:
                    time_index = col_index
            else:
                # continue
                # test for digits
                if self.allow_char:
                    allowed_cols.append(col_index)
                else:
                    if col_value.replace('.', '', 1).isdigit() or col_value.isdigit():
                        allowed_cols.append(col_index)
        return time_index, allowed_cols

    @staticmethod
    def test_time(date_str):
        # add all the possible formats
        try:
            if type(int(date_str)):
                return False, False
        except ValueError:
            try:
                if type(float(date_str)):
                    return False, False
            except ValueError:
                try:
                    date_time = parse(date_str)
                    t_stamp = time.mktime(date_time.timetuple())
                    return True, t_stamp
                except ValueError:
                    # raise ValueError('Python Error: no valid date-time format found')
                    return False, False

    @staticmethod
    def read_csv(file_path):
        # 1. retrieve data-set from file
        with open(file_path, 'r') as f:
            dialect = csv.Sniffer().sniff(f.readline(), delimiters=";,' '\t")
            f.seek(0)
            reader = csv.reader(f, dialect)
            temp = list(reader)
            f.close()
        return temp
