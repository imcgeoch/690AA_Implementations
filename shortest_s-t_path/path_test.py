from path import *
import networkx as nx
import math
import random
import itertools

# number of graphs to test
samples = 1000
# expected number of nodes in the graphs
n = 60
# expected proportion of edges the random graph has
p = 0.5

def get_random_instance():
    random_n = n + int(50 * random.random() - 25)
    graph = nx.erdos_renyi_graph(random_n,
                                 p * 2 * random.random())
    for (u,v,w) in graph.edges(data=True):
        w['weight'] = random.randint(1,100)
    s = random.randint(0, random_n-1)
    t = random.randint(0, random_n-1)
    return graph, s, t

def get_opt_length(graph, s, t):
    try:
        return nx.dijkstra_path_length(graph, s, t)
    except:
        return None

# if path is a path it returns the sum of the edges in the path
def get_path_length(graph, path):
    assert(len(path) >= 1)
    s = path[0]
    length = 0
    for i in range(1, len(path)):
        length += graph.get_edge_data(s, path[i])['weight']
        s = path[i]
    return length

for _ in range(samples):
    graph, s, t = get_random_instance()
    adj = nx.to_numpy_matrix(graph)
    adj[adj == 0] = np.inf
    np.fill_diagonal(adj, 0)
    alg_path = stpath(adj, s, t)
    opt_length = get_opt_length(graph, s, t)
    # if s and t are not connected the follow if stament will execute
    if opt_length == None or alg_path == None:
        assert(alg_path == opt_length)
        continue
    assert(alg_path[0] == s)
    assert(alg_path[-1] == t)
    alg_length = get_path_length(graph, alg_path)
    assert(alg_length == opt_length)
