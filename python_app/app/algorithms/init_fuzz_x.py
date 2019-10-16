# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "10 October 2019"

"""
import json
from algorithms.fuzz_x import FuzzX
from algorithms.init_data import InitData
from algorithms.aco_grad import GradACO
from data.sample_data import *


def init_algorithm(input_data):
    try:
        input_data = get_sample_data()
        obj = FuzzX(input_data)
        x_data = obj.cross_data()

        d_set = InitData(x_data)
        if d_set.data:
            steps = obj.steps
            max_combs = obj.combs
            min_supp = obj.min_sup

            d_set.init_attributes(False)
            ac = GradACO(steps, max_combs, d_set)
            list_gp = ac.run_ant_colony(min_supp)
            list_gp.sort(key=lambda k: (k[0], k[1]), reverse=True)

            list_pattern = list()
            for gp in list_gp[:4]:
                pattern = gp[1]
                support = gp[0]
                plot_data = generate_plot_data(d_set.title, pattern)
                list_pattern.append(([plot_data, "support:"+str(support)]))
            figure = GradACO.plot_patterns(list_pattern)
            return figure
    except Exception as error:
        print(error)


def generate_plot_data(list_title, list_pattern):
    plot_data = list()
    for pattern in list_pattern[:4]:
        i = int(pattern[0])
        name = get_attr_name(list_title, i)
        value = 0
        sign = pattern[1]
        if sign == '-':
            value = -1
        elif sign == '+':
            value = 1
        var_temp = {name: value}
        plot_data.append(var_temp)
    return plot_data


def get_attr_name(list_title, index):
    name = ""
    for title in list_title:
        i = int(title[0])
        if i == index:
            return title[1]
    return name
