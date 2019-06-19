#%%

import glob
import json
import pickle

import numpy as np
import os
import matplotlib.pyplot as plt
from axelrod import (get_largest_component_size, get_largest_domain_size,
                     get_local_avg_clustering, get_num_active_connections,
                     n_realizations, nodesNum)


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
    dict_of_variables["q"] = [int(i) for i in dict_of_variables["q"]]
    return dict_of_variables


def create_dict_of_graphs(data):
    dict_of_graphs = {}
    for q in data:
        dict_of_graphs["q"] = []


def load_all_pickle_data():
    dict_of_graphs = {}
    for filename in glob.glob('*.pickle'):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            for q in data:
                # print(q)
                if q in dict_of_graphs.keys():
                    dict_of_graphs[q]+=data[q]
                else:
                    dict_of_graphs[q] = data[q]
    return dict_of_graphs


def get_data_from_graphs(dict_of_graphs):
    out_simulation_data = {}
    for q in dict_of_graphs:

########################################################################################################################
##################     Tutaj mozna dodawac funkcje ktore chcemy policzyc na grafach

        global_clustering_sum = 0
        local_clustering_sum = 0
        relative_largest_component_sum = 0
        relative_largest_domain_sum = 0
        ##tu dodaj sume =0, sluzy do usredniania po kilku przebiegach dla danego q
        n=len(dict_of_graphs[q])
        for g in dict_of_graphs[q]:
            global_clustering = g.transitivity_undirected()
            local_clustering = get_local_avg_clustering(g)
            relative_largest_component = get_largest_component_size(g) / nodesNum
            relative_largest_domain = get_largest_domain_size(g) / nodesNum
            ##tutaj dopisz w jaki sposob policzyc dana wielkosc


            #dodatkowy warunek, jesli zdazyloby sie, ze jakis element daje wartosc nan
            if (np.isnan(global_clustering) or
                np.isnan(local_clustering) or
                np.isnan(relative_largest_component)):
                print("nan dla q = ",q)
                n-=1
                continue

            global_clustering_sum += global_clustering
            local_clustering_sum += local_clustering
            relative_largest_component_sum += relative_largest_component
            relative_largest_domain_sum += relative_largest_domain
            ##dodaj do sumy
        out_from_q_simulations = {"global_clustering": global_clustering_sum / n,
                                  "local_clustering": local_clustering_sum / n,
                                  "relative_largest_component": relative_largest_component_sum / n,
                                  "relative_largest_domain": relative_largest_domain_sum / n}
                                   ##dopisz nazwe i wartosc aby dodac do wykresu
########################################################################################################################

        out_simulation_data[str(q)] = out_from_q_simulations

    return out_simulation_data


def clean_data(data):
    dict_of_variables = create_dict_of_variables(data)
    add_data_to_dict_of_variables(data, dict_of_variables)
    dict_of_variables["q"] = [int(i) for i in dict_of_variables["q"]]
    return dict_of_variables


def save_dict(data,filename):
    json.dump( data, open( filename, 'w' ) )


def load_dict(filename):
    data = json.load( open( filename ) )
    return data
#%%
if __name__ == "__main__":
    JSON_NAME="model_a.json"
    if os.path.exists(JSON_NAME):
        pass
    else:    
        #wczytuje dane z pliku pickle
        dict_of_graphs = load_all_pickle_data()
        dict_of_data = get_data_from_graphs(dict_of_graphs)
        dict_of_variables = clean_data(dict_of_data)

        save_dict(dict_of_variables,JSON_NAME)
#%%
    dict_of_variables=load_dict(JSON_NAME)
    plt.figure()

    for element in dict_of_variables:
        if element != "q":
            plt.plot(dict_of_variables["q"], dict_of_variables[element], 'o', label=element)

    plt.legend()
    plt.xscale('log')
    plt.savefig('out.png')

    # plt.plot(dict_of_variables["q"], dict_of_variables["global_clustering"],'o')
    # plt.show()

#%%


