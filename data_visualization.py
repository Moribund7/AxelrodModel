import json
import pickle

import matplotlib.pyplot as plt
import glob
from axelrod import get_largest_component_size, get_local_avg_clustering, get_num_active_connections, nodesNum, \
    n_realizations


def create_dict_of_variables(data):
    dict_of_variables = {}
    for q in data:
        dict_of_variables["q"] = []
        for key in data[q].keys():
            key_str = str(key)
            dict_of_variables[key_str] = []
    return dict_of_variables


def add_data_to_dict_of_variables(data, dict_of_variables):
    for q in data:
        dict_of_variables["q"].append(q)
        for element in data[q]:
            dict_of_variables[element].append(data[q][element])


def load_all_json_data():
    dict_of_variables = None
    for filename in glob.glob('*.json'):
        with open(filename, "r") as f:
            data = json.load(f)
        if dict_of_variables == None:
            dict_of_variables = create_dict_of_variables(data)
        add_data_to_dict_of_variables(data, dict_of_variables)
    dict_of_variables["q"]=[int(i) for i in dict_of_variables["q"]]
    return dict_of_variables


def create_dict_of_graphs(data):
    dict_of_graphs = {}
    for q in data:
        dict_of_graphs["q"] = []


def load_all_pickle_data():
    dict_of_graphs = {}
    for filename in glob.glob('*.pickle'):
        with open(filename,'rb') as f:
            data = pickle.load(f)
            for q in data:
                print(q)
                if q in dict_of_graphs.keys():
                    dict_of_graphs[q].append[data[q]]
                else:
                    dict_of_graphs[q]=data[q]
    return dict_of_graphs

def get_data_from_graphs(dict_of_graphs):
    out_simulation_data={}
    for q in dict_of_graphs:
        global_clustering_sum=0
        local_clustering_sum=0
        relative_largest_component_sum=0

        for g in dict_of_graphs[q]:
            global_clustering = g.transitivity_undirected()
            local_clustering = get_local_avg_clustering(g)
            relative_largest_component = get_largest_component_size(g) / nodesNum

        global_clustering_sum += global_clustering
        local_clustering_sum += local_clustering
        relative_largest_component_sum += relative_largest_component


        out_from_q_simulations = {"global_clustering": global_clustering_sum / n_realizations,
                                  "local_clustering": local_clustering_sum / n_realizations,
                                  "relative_largest_component": relative_largest_component_sum / n_realizations}

        out_simulation_data[str(q)] = out_from_q_simulations

    return out_simulation_data

if __name__ == "__main__":

    dict_of_graphs = load_all_pickle_data()
    dict_of_variables=get_data_from_graphs(dict_of_graphs)

    plt.figure()

    for element in dict_of_variables:
        if element != "q":
            plt.plot(dict_of_variables["q"], dict_of_variables[element], 'o', label=element)

    plt.legend()
    plt.xscale('log')
    plt.savefig('out.pdf')

    # plt.plot(dict_of_variables["q"], dict_of_variables["global_clustering"],'o')
    # plt.show()