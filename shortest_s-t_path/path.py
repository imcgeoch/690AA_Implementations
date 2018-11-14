"""
An Implementation of a Primal-Dual approach to shortest s-t path
"""
import numpy as np


def stpath(G, s, t):
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
    n = G.shape[0]
    x = np.zeros_like(G)
    F = []
    C = [s]

    while not t in C:
        # Find all the edges that cross
        deltaC = [(i, j, G[i, j] - x[i, j]) for i in xrange(n)
                  for j in xrange(n) if i in C and not j in C]
        # Find the amount they will all increase by and the edge that is
        # met with equality
        newEdge = min(deltaC, key=lambda edge: edge[2])
        # Increase the primal variable for all edges that cross
        y_C = newEdge[2]

        # If all crossing edges are of infinite weight, there is no path.
        if y_C == np.inf:
            return None
        for i, j, _ in deltaC:
            x[i, j] += y_C
            x[j, i] += y_C

        # Add the edge that was met with equality to F
        F.append(newEdge[0:2])
        C.append(newEdge[1])

    # Find the path from s to t. F must be a tree so there is only one.
    path = search(s, t, F)
    return path

def search(s, t, F):
    """
    Runs a DFS on a tree.

    Args:
        s: The start vertex given as an int
        t: The end vertex given as an int
        F: A tree given as an adjacency list.
           For any edge (i,j) in F, i must be closer to s.
    """

    # A dictionary of predecessors.
    preds = {}
    path = []

    stack = [s]
    preds[s] = -1

    # DFS from s to t, leaving breadcrumbs in the dictionary.
    while stack:
        v = stack.pop()
        if v == t:
            break
        for i, j in F:
            if i == v:
                preds[j] = v
                stack.append(j)

    # Walk back along the breadcrumbs.
    while v != -1:
        path.append(v)
        v = preds[v]

    return path[::-1]

def main():
    """
    The main method. Nothing here.
    """
    pass

if __name__ == "__main__":
    main()
