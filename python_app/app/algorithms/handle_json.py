# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor",
@credits: "Thomas Runkler, Edmond Menya, and Anne Laurent",
@license: "MIT",
@version: "1.0",
@email: "owuordickson@gmail.com",
@created: "12 July 2019",
@modified: "26 February 2020",

"""
from handle_data import HandleData


class InitData(HandleData):

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

