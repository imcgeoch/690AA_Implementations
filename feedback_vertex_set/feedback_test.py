from feedback import *
import networkx as nx
import matplotlib.pyplot as plt
import math
import random
import itertools
import time

# number of graphs to test
samples = 1000
# number of nodes in the graphs
n = 7
# proportion of edges
p = .5

options = {
    'node_color': 'C0',
    'node_size': 5,
}
# to draw a particular networkx graph run
#nx.draw_spectral(graph, **options)
#plt.show()

# weights are integer with probability 1/2 else float
def get_random_instance():
    nn = n + int(5 * random.random())
    pp = p * random.random()
    graph = nx.erdos_renyi_graph(nn, pp)
    if bool(random.getrandbits(1)):
        weights = np.round(np.random.uniform(100, 1, nn))
    else:
        weights = np.random.uniform(100, 1, nn)
    return graph, weights

# returns whether the provided set is an fvs for graph
def verify_fvs(graph, fvs):
    g = graph.copy()
    g.remove_nodes_from(fvs)
    try:
        nx.find_cycle(g)
    except:
        return True
    return False

# returns the optimal fvs for graph
# checks all possible selections of vertices and keeps track of the best fvs seen so far
def optimal_fvs(graph, weights):
    if verify_fvs(graph, []):
        return [], 0
    optSol = []
    optWeight = np.inf
    size = len(graph.nodes())
    vertices = list(graph.nodes())
    for x in range(size - 2, 0, -1):
        combo = itertools.combinations(vertices, x)
        for y in combo:
            if verify_fvs(graph, y):
                weight = np.sum(weights[list(y)])
                if weight <= optWeight:
                    optWeight = weight
                    optSol = y
    return optSol, optWeight


for _ in range(samples):
    graph, weights = get_random_instance()
    approx = feedback_vertex(nx.to_numpy_matrix(graph), weights)
    approx_weight = np.sum(weights[approx])
    _, opt_weight = optimal_fvs(graph, weights)
    # verifies the approximate min fvs is a loop cut set
    assert(verify_fvs(graph, approx) == True)
    # verifies this instance achieves the claimed bounds
    assert(approx_weight <= 4*math.ceil(math.log(n))*opt_weight)
    print("pass")
