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


def init_algorithm():
    try:
        path = '../data/dataset.json'
        obj = FuzzX(path)
        x_data = obj.cross_data()
        # print(obj.observation_list)
        # print(x_data)

        d_set = InitData(x_data)
        if d_set.data:
            steps = obj.steps
            max_combs = obj.combs
            min_supp = obj.min_sup

            list_attr = list()
            for txt in d_set.title:
                text = str(txt[0]) + '. ' + txt[1]
                var_attr = {"attribute": text}
                list_attr.append(var_attr)
                # print(var_attr)
            # print("\nFile: " + "none")

            d_set.init_attributes(False)
            ac = GradACO(steps, max_combs, d_set)
            list_gp = ac.run_ant_colony(min_supp)
            # print("\nPattern : Support")
            list_pattern = list()
            for gp in list_gp[:5]:
                pattern = str(gp[1])
                support = str(gp[0])
                var_pattern = {"pattern": pattern, "support": support}
                list_pattern.append(var_pattern)
                # print(var_pattern)
            # p_data = ac.plot_pheromone_matrix()
            # print(p_data)
            json_response = json.dumps({"attributes": list_attr, "patterns": list_pattern})
            return json_response
            # print(json_response)
            # print("\nPheromone Matrix")
            # print(ac.p_matrix)
            # ac.plot_pheromone_matrix()
    except Exception as error:
        print(error)


init_algorithm()
