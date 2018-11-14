import numpy as np

"""
An Implementation of a Primal-Dual approach to shortest s-t path
"""

def stpath(G,s,t):
    """
    A Primal-Dual approach to the shortest s-t path problem. Equivalent
    to Dijkstra's Algorithm

    Args:
        G: A 2-d numpy array representing the graph as an adjacency matrix.
           G(i,j) is the cost of an edge from i to j. should be np.inf 
           if no edge exists.
        s: The start vertex, given as an integer 0 <= s < n
        t: The end vertex, given as an integer 0 <= t < n, s != t
    """

    H = G.copy()
    # The connected component
    n = G.shape[0]
    F = []

    C = [s]
    while not t in C:
        crossingEdges = [(i,j,H[i,j]) for i in xrange(n) for j in xrange(n) 
                         if i in C and not j in C]
        if crossingEdges == []:
            return None
        newEdge = min(crossingEdges, key = lambda edge: edge[2])
        F.append(newEdge[0:2])
        y_C = newEdge[2]
        C.append(newEdge[1])

        for i, j, w in crossingEdges:
            H[i,j] -= y_C
            H[j,i] -= y_C

    np.set_printoptions(precision=3)
    print [((i,j), G[i,j]) for i, j in F]
    
    path = search(s, t, F)
    return path

def search(s, t, F):
    preds = {}
    path = []

    stack = [s]
    preds[s] = -1
    while stack:
        v = stack.pop()
        if v == t:
            break
        for i, j in F:
            if i == v:
                preds[j] = v
                stack.append(j)
    
    while v != -1:
        path.append(v)
        v = preds[v]

    return path[::-1]


def main():
    pass

if __name__ == "__main__":
    main()
