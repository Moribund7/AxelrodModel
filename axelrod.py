import igraph
import numpy as np

def newNeighbourModelA(g,node):
    t=[]
    for i in range(0,g.vcount()):
        for j in range(g.degree(i)):
            t.append(i)
    newNeighbour = node
    while(newNeighbour==node):
        newNeighbour=np.random.choice(t)
    return newNeighbour

def getLargestComponentSize(g): 
    return max([np.size(g.components()[i]) for i in range(len(g.components()))])


def getNumActiveConnections(g):
    activeEdges=0
    F=len(g.vs.attributes())
    for i in range(g.vcount()):
        for j in g.neighbors(i):
            flag=False
            for k in range(F):
                if(g.vs[i][str(k)]!=g.vs[j][str(k)]):
                    flag=True
                    break
            if(flag):
                activeEdges+=1
    return activeEdges/2 
        
def evolve(g,newNeighbourFun):
    frozen=False
    F=len(g.vs.attributes())
    t=0
    while(not frozen):
        t+=1
        if(not (t%10000)):
            numActiveConnections=getNumActiveConnections(g)
            print("t= ",t," active: ",numActiveConnections)
            if(numActiveConnections == 0):
                frozen=True
        a = np.random.randint(0,g.vcount())
        if(g.neighbors(a)==[]):
            continue
        b = np.random.choice(g.neighbors(a))
        differentTraits=[]
        for trait in range(F):
            if(g.vs[a][str(trait)]!=g.vs[b][str(trait)]):
                differentTraits.append(trait)
        if(len(differentTraits)==0): ### takie same traity - nic się nie dzieje
            continue
        if(len(differentTraits)==F): ### zupełnie różne traity - rozłączenie
            newNeighbour=newNeighbourFun(g,a)
            g.delete_edges((a,b))
            g.add_edges([(a,newNeighbour)])
        else:                       ### zmiana cechy
            if(np.random.rand() > len(differentTraits)/F):
                traitToChange=np.random.choice(differentTraits)
                g.vs[a][str(traitToChange)]=g.vs[b][str(traitToChange)]


## generacja randomowego grafu z randomowym traitami
nodesNum=500
F=3 
q=1000 
g=igraph.Graph.Erdos_Renyi(n=nodesNum,m=nodesNum*2)

for i in range(F):
    g.vs[str(i)]=np.random.randint(0,q,nodesNum)

evolve(g,newNeighbourModelA)

print("gobal clustering ",g.transitivity_undirected())
print("largest component ",getLargestComponentSize(g),getLargestComponentSize(g)/nodesNum)