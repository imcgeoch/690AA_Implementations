"""
An implementation of an approximation algorithm for Feedback Vertex Set.
Gives a log(n)-approximation.
"""
from collections import deque
import numpy as np


def feedback_vertex(G, w):
    """
    Finds a low-weight set of vertices that if remove make the graph
    acyclic. An approximation of the optimal set.

    Args:
        G: a 2-d numpy array representing the graph as an adjacency
           matrix.
        w: a 1-d numpy array containing the weights of the vertices.
    """
    G = np.copy(G)
    # The list of vertices found by the algortihm
    F = []
    # The weight for each
    x = np.zeros_like(w)

    # As long as cycles exist, Increase the "dual weight" of every
    # vertex by an amount equal to the smallest amount of headroom
    # remove the one that's met with equality from the graph and
    # add it to the solution set. Here, "removal" is acheived by
    # disconnecting the vertex.
    while remove_vertices(G):
        cycle = find_cycle(G)
        headrooms = w[cycle] - x[cycle]

        x[cycle] += min(headrooms)
        vertexMet = cycle[np.argmin(headrooms)]

        F.append(vertexMet)
        G[vertexMet] = 0
        G[:, vertexMet] = 0

    return F

def remove_vertices(G):
    """
    Repeatedly removes degree-one vertices from a graph until no more
    remain. "Removal" is acheived by disconnecting the vertices.
    Modifies the input in place.

    Args:
        G: a 2-d numpy array representing the graph as an adjacency
           matrix. This object will be modified.

    Returns:
        True if vertices remain, false otherwise.
    """
    degrees = G.sum(1)
    while 1 in degrees:
        ones = [i for i, j in enumerate(degrees) if j == 1]
        for i in ones:
            G[i] = 0
            G[:, i] = 0
        degrees = G.sum(1)
    return G.sum() != 0


def find_cycle(G):
    """
    Finds a cycle that includes at most 2log(n) vertices of degree at
    least 3

    Args:
        G: a 2-d numpy array representing the graph as an adjacency
           matrix. G must contain no vertices of degree 1.

    Returns:
        A list containing the vertices in the cycle, or None of none
        exists
    """
    degrees = G.sum(1)

    if max(degrees) == 2:
        return find_deg2_cycle(G)
    return find_deg3_cycle(G)

def find_deg2_cycle(G):
    """
    Finds a cycle in a graph where all vertices are of degree 2

    Args:
        G: a 2-d numpy array representing the graph as an adjacency
           matrix. G must contain only vertices of degree 2

    Returns:
        A list containing a=the vertices in the cycle.
    """

    cycle = []
    degrees = G.sum(1)
    # Pick an arbitrary vertex of degree 2.
    for i, j in enumerate(degrees):
        if j == 2:
            cycle.append(i)
            break
    current = cycle[0]

    prev = -1
    while True:
        neighbor = [i for i, j in enumerate(G[current])
                    if j == 1 and i != prev][0]
        prev = current
        current = neighbor
        if current == cycle[0]:
            break
        else:
            cycle.append(current)

    return cycle

def find_deg3_cycle(G):
    """
    Finds a cycle in a graph with at least one vertex of degree 3

    Args:
        G: a 2-d numpy array representing the graph as an adjacency
           matrix. G must contain no vertices of degree 1 and at least
           one of degree 3 or greater

    Returns:
        A list containing the vertices in the cycle, not nessecarily
        in order.
    """

    # A dictionary of predecessors; serves as a trail of breadcrumbs.
    predecessors = {}

    queue = deque()
    degrees = G.sum(1)

    # Identify a starting vertex.
    for i, j in enumerate(degrees):
        if j > 2:
            queue.append(i)
            predecessors[i] = -1
            break

    # Run a modified BFS. When finding a path of degree-2 vertices,
    # follow all the way along it. Stop when reaching a visited vertex.
    # this search will find a cycle with a minimum number of vertices
    # of degree at least 3.
    while queue:
        current = queue.popleft()
        neighbors = [i for i, j in enumerate(G[current]) if j == 1
                     and i != predecessors[current]]

        for neighbor in neighbors:

            # Follow paths degree 2 vertices as far as possible. Because
            # the graph contains no degree-1 vertices we don't have to
            # worry about them.
            pathcurrent = current
            while degrees[neighbor] < 3:
                # Look at the neighbor's neighbors, pick the one that
                # does not double back.
                predecessors[neighbor] = pathcurrent
                nn = [i for i, j in enumerate(G[neighbor])
                      if j == 1 and i != pathcurrent][0]
                pathcurrent = neighbor
                neighbor = nn
            # If we've found an already-visited vertex, stop and
            # calculate a cycle using the predecessor dictionary.
            # Otherwise push the neighbor into the queue.
            if neighbor in predecessors:
                return backtrace_cycle(predecessors, neighbor, pathcurrent)
            else:
                queue.append(neighbor)
                predecessors[neighbor] = pathcurrent
    # If nothing was found, return None. This won't ever happen.
    return None

def backtrace_cycle(preds, start, end):
    """
    Given a dict of predecessors from a search, walks pack to find a
    cycle

    Args:
        preds: a dictionary of predecessors
        start: the beginning of the cycle found by the search
        end: the end of the cycle found by the search
    Returns:
        The vertices in the cycle, not nessecarily in order.
    """
    cycle = []
    startpath = []
    endpath = []
    while start != -1:
        startpath.append(start)
        start = preds[start]
    while end != -1:
        endpath.append(end)
        end = preds[end]
    for i in startpath:
        cycle.append(i)
        if i in endpath:
            break
    for j in endpath:
        if j in startpath:
            break
        cycle.append(j)
    return cycle

def main():
    """
    The main method contains two simple test cases.
    """
    # A couple of test cases

    G1 = np.array([[0, 1, 0, 1],
                   [1, 0, 1, 0],
                   [0, 1, 0, 1],
                   [1, 0, 1, 0]])
    G2 = np.array([[0, 1, 1, 0, 0, 0],
                   [1, 0, 1, 0, 0, 0],
                   [1, 1, 0, 1, 0, 0],
                   [0, 0, 1, 0, 1, 1],
                   [0, 0, 0, 1, 0, 1],
                   [0, 0, 0, 1, 1, 0]])
    w1 = np.array([3, 2, 1, 9])
    w2 = np.array([2, 6, 4, 9, 1, 7])

    print feedback_vertex(G1, w1)
    print feedback_vertex(G2, w2)

if __name__ == '__main__':
    main()
