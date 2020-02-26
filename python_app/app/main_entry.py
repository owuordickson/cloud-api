# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Anne Laurent and Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"
@created: "25 February 2020"

"""

import json
import matplotlib.pyplot as plt
import pandas
from itertools import cycle, islice
from io import BytesIO
import base64
from algorithms.tx_json import FuzzTXj
from algorithms.handle_json import InitData
from algorithms.aco_grad import GradACO


def init_request(req_data):
    try:
        json_data = read_json(req_data)
        pattern = json_data["patternType"]
        min_sup = json_data["minSup"]
        #datastreams = json_data["datastreams"]
        x_data = cross_data(json_data)
        if pattern == "ftgp":
            ref_col = json_data["c_ref"]
            min_rep = json_data["m_rep"]
            title, list_gp = init_acotgraank(x_data, min_sup, min_rep, ref_col)
        else:
            title, list_gp = init_acograd(x_data, min_sup)

        list_pattern = list()
        for gp in list_gp[:4]:
            pattern = gp[1]
            support = gp[0]
            plot_data = generate_plot_data(title, pattern)
            list_pattern.append(([plot_data, "support:"+str(support)]))
        figure = plot_patterns(list_pattern)
        return figure
    except Exception as error:
        #print error
        raise ValueError(error)


def read_json(data):
    # with open(file, 'r') as f:
    temp_data = json.loads(data)
    return temp_data


def cross_data(raw_data):
    try:
        obj = FuzzTXj(raw_data)
        x_data = obj.cross_data()
        if x_data:
            return x_data
        else:
            raise Exception("Crossing Error: Unable to cross data")
    except Exception as error:
        raise Exception(error)


def init_acograd(data, min_sup):
    d_set = InitData(data)
    if d_set.data:
        d_set.init_attributes(False)
        ac = GradACO(d_set)
        list_gp = ac.run_ant_colony(min_sup)
        list_gp.sort(key=lambda k: (k[0], k[1]), reverse=True)
        return d_set.title, list_gp
    else:
        raise Exception("Mining Error: Unable to fetch patterns")


def init_acotgraank(data, min_sup, min_rep, ref_col):
    return "title", list()


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


def plot_patterns(list_pattern):
    num = len(list_pattern)
    count = 0
    if num == 1:
        df = pandas.DataFrame(list_pattern[count][0])
        my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k']), None, len(df)))
        ax = df.plot(kind='bar', stacked=True, width=1, color=my_colors)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_position('center')
        plt.ylim(-2, 2)
        plt.xlim(-0.5, len(list_pattern[count][0]))
        plt.yticks([-1, 1], ['-', '+'])
        plt.xticks([], [])
        plt.text(0, 1.8, list_pattern[count][1])
    elif num == 2:
        fig, axes = plt.subplots(2)
        for r in range(2):
            df = pandas.DataFrame(list_pattern[count][0])
            my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k']), None, len(df)))
            df.plot(ax=axes[r], kind='bar', stacked=True, width=1, color=my_colors)
            axes[r].spines['right'].set_visible(False)
            axes[r].spines['top'].set_visible(False)
            axes[r].spines['bottom'].set_position('center')
            # axes[r, c].set_title("support: "+str(count))
            axes[r].text(0, 1.8, list_pattern[count][1])
            axes[r].set_xlim([-0.5, len(list_pattern[count][0])])
            axes[r].set_ylim([-2, 2])
            count += 1
        plt.setp(axes, xticks=[], xticklabels=[], yticks=[-1, 1], yticklabels=['-', '+'])
    elif num == 3:
        fig, axes = plt.subplots(2, 2)
        for r in range(2):
            for c in range(2):
                if count <= 2:
                    df = pandas.DataFrame(list_pattern[count][0])
                    my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k']), None, len(df)))
                    df.plot(ax=axes[r, c], kind='bar', stacked=True, width=1, color=my_colors)
                    axes[r, c].spines['right'].set_visible(False)
                    axes[r, c].spines['top'].set_visible(False)
                    axes[r, c].spines['bottom'].set_position('center')
                    # axes[r, c].set_title("support: "+str(count))
                    axes[r, c].text(0, 1.8, list_pattern[count][1])
                    axes[r, c].set_xlim([-0.5, len(list_pattern[count][0])])
                    axes[r, c].set_ylim([-2, 2])
                    count += 1
        plt.setp(axes, xticks=[], xticklabels=[], yticks=[-1, 1], yticklabels=['-', '+'])
    elif num == 4:
        fig, axes = plt.subplots(2, 2)
        for r in range(2):
            for c in range(2):
                df = pandas.DataFrame(list_pattern[count][0])
                my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k']), None, len(df)))
                df.plot(ax=axes[r, c], kind='bar', stacked=True, width=1, color=my_colors)
                axes[r, c].spines['right'].set_visible(False)
                axes[r, c].spines['top'].set_visible(False)
                axes[r, c].spines['bottom'].set_position('center')
                # axes[r, c].set_title("support: "+str(count))
                axes[r, c].text(0, 1.8, list_pattern[count][1])
                axes[r, c].set_xlim([-0.5, len(list_pattern[count][0])])
                axes[r, c].set_ylim([-2, 2])
                count += 1
        plt.setp(axes, xticks=[], xticklabels=[], yticks=[-1, 1], yticklabels=['-', '+'])
    else:
        plt.title("No Patterns Found")
    fig_bytes = BytesIO()
    plt.savefig(fig_bytes, format='png')
    fig_bytes.seek(0)  # rewind to beginning of file
    buffer = b''.join(fig_bytes)
    fig_base64 = base64.b64encode(buffer)
    img_data = fig_base64.decode('utf-8')
    return img_data