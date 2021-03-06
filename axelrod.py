# -*- coding: utf8 -*-
n_realizations=2 #po ilu realizacjach dla kazdej wartosc q usredniamy

import datetime
import pickle

import igraph
import numpy as np

def plot_graph(g):
    g.vs["label"] = [str(g.vs["0"][i])+str(g.vs['2'][i])+str(g.vs['2'][i]) for i in range(len(g.vs['0']))]

    igraph.plot(g,vertex_size=40)

def new_neighbour_model_a(g, node):
    t = []
    for i in range(0, g.vcount()):  # dla kazdego noda
        for j in range(g.degree(i)):  # dodajemy go tyle razy ile ma polaczen
            t.append(i)
    new_neighbour = node
    i=0
    while new_neighbour == node or (new_neighbour in g.neighbors(node)):
        new_neighbour = np.random.choice(t)
    return new_neighbour

import random
def new_neighbour_model_f(g, node):
    '''
    Wybieramy nowego sasiada node jako jednego z sasiadow jego
    sasiadow. Jesli nie ma takich wtedy wybieramy losowy wezel
    '''
    t = []
    for neighbourNode in g.neighbors(node):
        t.append(g.neighbors(neighbourNode))
    tFlat = [item for sublist in t for item in sublist]
    #remove node from list
    tFlat=[x for x in tFlat if x != node]
    i = 0
    random.shuffle(tFlat)
    
    for new_neighbour in tFlat:
        if (new_neighbour == node or (new_neighbour in g.neighbors(node))):
            pass
        else:
            return new_neighbour
    
    #return random node
    new_neighbour = node
    print(tFlat)
    print("brak kolegow")
    while new_neighbour == node or (new_neighbour in g.neighbors(node)):
        new_neighbour = np.random.randint(0,nodesNum)
        
    return new_neighbour


def get_largest_component_size(g):
    return max([np.size(g.components()[i]) for i in range(len(g.components()))])


def get_num_active_connections(g):
    active_edges = 0
    F = len(g.vs.attributes()) if 'label' not in g.vs.attributes() else len(g.vs.attributes())-1 #rysowanie daje label jako atrybut
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
    F = len(g.vs.attributes()) if 'label' not in g.vs.attributes() else len(
        g.vs.attributes()) - 1  # rysowanie daje label jako atrybut
    t, c = 0, 0
    tInterval, checkInterval = 10000, 20
    # tInterval = co ile t sprawdzane są aktywne połączenia
    # checkInterval jeśli po tylu sprawdzeniach t jest ciągle tyle samo aktywnych połączeń uznajemy że dalej się nic nie zmieni
    activeConnectionsHistory = list(range(0, 30))  # cokolwiek niestałego

    while not frozen:
        t += 1
        if not (t % 10000):
            numActiveConnections = get_num_active_connections(g)
            print("q= ", q, "t= ", t, " active: ", numActiveConnections)
            activeConnectionsHistory.append(numActiveConnections)

            if (numActiveConnections == 0):
                frozen = True
            if (sum(activeConnectionsHistory[-checkInterval:]) / checkInterval == activeConnectionsHistory[-1]):
                frozen = True
        a = np.random.randint(0, g.vcount())
        if not g.neighbors(a):
            continue
        b = np.random.choice(g.neighbors(a))
        differentTraits = []
        for trait in range(F):
            if g.vs[a][str(trait)] != g.vs[b][str(trait)]: #no asci character ?
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


def sameAtributes(g,v1,v2):
    F = len(g.vs.attributes()) if 'label' not in g.vs.attributes() else len(g.vs.attributes()) - 1  # rysowanie daje label jako atrybut
    differentTraits = []
    for trait in range(F):
        if g.vs[v1][str(trait)] != g.vs[v2][str(trait)]:
            differentTraits.append(trait)
    if(len(differentTraits)==0):
        return True
    else:
        return False

def domain_bfs(g, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if (vertex not in visited) and sameAtributes(g,vertex,start):
            visited.add(vertex)
            queue.extend(set(g.neighborhood(vertex)) - visited)
    return visited

def get_largest_domain_size(g):
    domains=[]
    nodesToCheck=set(range(0,g.vcount()))
    while bool(nodesToCheck):
        i=nodesToCheck.pop()
        domain=domain_bfs(g,i)
        domains.append(domain)
        nodesToCheck=nodesToCheck-domain
    return max([len(domains[i]) for i in range(len(domains))])

#hiperparametry
nodesNum = 500


if __name__ == "__main__":

    q_list = [int(np.sqrt(2) ** q) for q in range(1, 500, 1) if
              int(np.sqrt(2) ** q) > 3 and int(np.sqrt(2) ** q) < 10500]
    # wartosci q dla ktorych symulujemy
    q_list[1] = 6 # podmieniamy q==5 na q==6 (ladniej wyglada na wykresie)
    out_simulation_data=dict() # przechowuje wyniki symulacji
    output_path="data"+str(q_list)+str(datetime.datetime.now().timestamp())+'.pickle'


    # generacja randomowego grafu z randomowym traitami

    F = 3

    for q in q_list:
        graphs_for_q_list=[]
        for realization in range(n_realizations):
            # tworzymy losowy graf z nodeNum*2 polaczeniami
            g = igraph.Graph.Erdos_Renyi(n=nodesNum, m=nodesNum * 2)

            # dla kazdej z F cech dla kazdego noda wybieramy wartosc z zakresu [0,q[
            for i in range(F):
                g.vs[str(i)] = np.random.randint(0, q, nodesNum)  # dlaczego jako string?

            evolve(g, new_neighbour_model_f)

            graphs_for_q_list.append(g)
        out_simulation_data[str(q)]=graphs_for_q_list

    with open(output_path, "wb") as f:
        pickle.dump(out_simulation_data, f)

