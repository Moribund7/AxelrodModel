import pickle

import igraph
import json
import numpy as np


def new_neighbour_model_a(g, node):
    t = []
    for i in range(0, g.vcount()):  # dla kazdego noda
        for j in range(g.degree(i)):  # dodajemy go tyle razy ile ma polaczen
            t.append(i)
    new_neighbour = node
    while new_neighbour == node:
        new_neighbour = np.random.choice(t)
    return new_neighbour


def get_largest_component_size(g):
    return max([np.size(g.components()[i]) for i in range(len(g.components()))])


def get_num_active_connections(g):
    active_edges = 0
    F = len(g.vs.attributes())
    for i in range(g.vcount()):
        for j in g.neighbors(i):
            flag = False
            for k in range(F):
                if g.vs[i][str(k)] != g.vs[j][str(k)]:
                    flag = True
                    break
            if flag:
                active_edges += 1
    return active_edges / 2


def evolve(g, new_neighbour_fun):
    frozen = False
    F = len(g.vs.attributes())
    t = 0
    while not frozen:
        t += 1
        if not (t % 10000):
            numActiveConnections = get_num_active_connections(g)
            print("t= ", t, " active: ", numActiveConnections)
            if numActiveConnections == 0:
                frozen = True
        a = np.random.randint(0, g.vcount())
        if not g.neighbors(a):
            continue
        b = np.random.choice(g.neighbors(a))
        differentTraits = []
        for trait in range(F):
            if g.vs[a][str(trait)] != g.vs[b][str(trait)]:
                differentTraits.append(trait)
        if len(differentTraits) == 0:  # takie same traity - nic się nie dzieje
            continue
        if len(differentTraits) == F:  # zupełnie różne traity - rozłączenie
            newNeighbour = new_neighbour_fun(g, a)
            g.delete_edges((a, b))
            g.add_edges([(a, newNeighbour)])
        else:  # zmiana cechy
            if np.random.rand() > len(differentTraits) / F:
                traitToChange = np.random.choice(differentTraits)
                g.vs[a][str(traitToChange)] = g.vs[b][str(traitToChange)]


def get_local_avg_clustering(g):
    local_list=g.transitivity_local_undirected(mode='zero')
    return sum(local_list)/len(local_list)

if __name__ == "__main__":
    #hiperparametry
    n_realizations=1 #po ilu realizacjach dla kazdej wartosc q usredniamy
    q_list=[2**q for q in range(2, 500, 1) if 2**q > 250 and 2**q < 1050] # wartosci q dla ktorych symulujemy
    out_simulation_data=dict() # przechowuje wyniki symulacji
    output_path="data"+str(q_list)+".pickle"


    # generacja randomowego grafu z randomowym traitami
    nodesNum = 500
    F = 3

    for q in q_list:
        graphs_for_q_list=[]
        for realization in range(n_realizations):
            # tworzymy losowy graf z nodeNum*2 polaczeniami
            g = igraph.Graph.Erdos_Renyi(n=nodesNum, m=nodesNum * 2)

            # dla kazdej z F cech dla kazdego noda wybieramy wartosc z zakresu [0,q[
            for i in range(F):
                g.vs[str(i)] = np.random.randint(0, q, nodesNum)  # dlaczego jako string?

            evolve(g, new_neighbour_model_a)

            graphs_for_q_list.append(g)

        out_simulation_data[str(q)]=graphs_for_q_list


    with open(output_path, "wb") as f:
        pickle.dump(out_simulation_data, f)

