# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor",
@credits: "Thomas Runkler, Edmond Menya, and Anne Laurent",
@license: "MIT",
@version: "1.0",
@email: "owuordickson@gmail.com",
@created: "12 July 2019",
@modified: "14 October 2019",

"""
import numpy as np


class InitData:

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.data = raw_data
        self.title = self.get_title()
        self.attr_index = self.get_attributes()
        self.column_size = self.get_attribute_no()
        self.size = self.get_size()
        self.thd_supp = False
        self.equal = False
        self.attr_data = []
        self.lst_bin = []

    def get_size(self):
        size = len(self.raw_data)
        return size

    def get_attribute_no(self):
        count = len(self.raw_data[0])
        return count

    def get_title(self):
        data = self.raw_data
        if data[0][0].replace('.', '', 1).isdigit() or data[0][0].isdigit():
            return False
        else:
            if data[0][1].replace('.', '', 1).isdigit() or data[0][1].isdigit():
                return False
            else:
                title = []
                for i in range(len(data[0])):
                    # sub = (str(i + 1) + ' : ' + data[0][i])
                    # sub = data[0][i]
                    sub = [str(i+1), data[0][i]]
                    title.append(sub)
                del self.data[0]
                return title

    def get_attributes(self):
        attr = []
        time_cols = InitData.get_time_cols()
        for i in range(len(self.title)):
            temp_attr = self.title[i]
            indx = int(temp_attr[0])
            if len(time_cols) > 0 and ((indx-1) in time_cols):
                # exclude date-time column
                continue
            else:
                attr.append(temp_attr[0])
        return attr

    def init_attributes(self, eq):
        # Arrange rank attributes to generate Graph attribute
        self.equal = eq
        temp = self.data
        cols = self.column_size
        time_cols = InitData.get_time_cols()
        for col in range(cols):
            if len(time_cols) > 0 and (col in time_cols):
                # exclude date-time column
                continue
            else:
                # get all tuples of an attribute/column
                raw_tuples = []
                for row in range(len(temp)):
                    raw_tuples.append(float(temp[row][col]))
                attr_data = [self.title[col][0], raw_tuples]
                self.attr_data.append(attr_data)

    def get_bin_rank(self, attr_data, symbol):
        n = len(attr_data[1])
        incr = tuple([attr_data[0], '+'])
        decr = tuple([attr_data[0], '-'])
        temp_pos = np.zeros((n, n), dtype='bool')
        temp_neg = np.zeros((n, n), dtype='bool')
        var_tuple = attr_data[1]
        for j in range(n):
            for k in range(j + 1, n):
                if var_tuple[j] > var_tuple[k]:
                    temp_pos[j][k] = 1
                    temp_neg[k][j] = 1
                else:
                    if var_tuple[j] < var_tuple[k]:
                        temp_neg[j][k] = 1
                        temp_pos[k][j] = 1
                    else:
                        if self.equal:
                            temp_neg[j][k] = 1
                            temp_pos[k][j] = 1
                            temp_pos[j][k] = 1
                            temp_neg[k][j] = 1
        temp_bin = np.array([])
        if symbol == '+':
            temp_bin = temp_pos
        elif symbol == '-':
            temp_bin = temp_neg
        supp = float(np.sum(temp_bin)) / float(n * (n - 1.0) / 2.0)
        self.lst_bin.append([incr, temp_pos, supp])
        self.lst_bin.append([decr, temp_neg, supp])
        return supp, temp_bin

    @staticmethod
    def get_time_cols():
        time_cols = list()
        time_cols.append(0)
        # time_cols.append(1)
        return time_cols
