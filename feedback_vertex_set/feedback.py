import numpy as np
from collections import deque


def feedback_vertex(G, w):
    # The list of vertices found by the algortihm
    F = []
    # The weight for each 
    x = np.zeros_like(w)
    
    # Increase the "dual weight" of every vertex
    # by an amount equal to the smallest amount of headroom
    # remove the one that's met with equality from the graph and 
    # add it to the solution set
    while(remove_vertices(G)):
        cycle = find_cycle(G)
        headrooms = w[cycle] - x[cycle]
        
        increase = min(headrooms)
        x[cycle] += increase
        
        F.append(cycle[np.argmin(headrooms)])

        for i in cycle:
            if x[i] == w[i]:
                G[i] = 0
                G[:,i] = 0

    return F

"""
Repeatedly removes degree-one vertices from a graph until no more remain

Args:
    G: a 2-d numpy array representing the graph as an adjacency matrix. This object
       will be modified. 

Returns:
   True if vertices remain, false otherwise.
"""
def remove_vertices(G):
    degrees = G.sum(1)
    while 1 in degrees:
        ones = [i for i,j in enumerate(degrees) if j ==1]
        for i in ones:
            G[i] = 0
            G[:,i] = 0
        degrees = G.sum(1)
    return G.sum() != 0


"""
Finds a cycle that includes at most 2log(n) vertices of degree at least 3

Args:
    G: a 2-d numpy array representing the graph as an adjacency matrix. 
       G must contain no vertices of degree 1. 

Returns:
    A list containing the vertices in the cycle, or None of none exists
"""
def find_cycle(G):
    degrees = G.sum(1)

    if max(degrees) == 2:
        return find_deg2_cycle(G)
    else: 
        return find_deg3_cycle(G)

"""
Finds a cycle in a graph where all vertices are of degree 2

Args:
    G: a 2-d numpy array representing the graph as an adjacency matrix. 
       G must contain only vertices of degree 2

Returns:
    A list containing a=the vertices in the cycle.
"""
def find_deg2_cycle(G):

    cycle = []
    degrees = G.sum(1)
    for i, j in enumerate(degrees):
        if j == 2:
            cycle.append(i)
            break
    current = cycle[0]
    
    prev = -1
    while True:
        neighbors = [i for i,j in enumerate(G[current]) if j == 1]
        # One of the neighbors is the one we want to continue to
        for neighbor in neighbors:
            if neighbor != prev:
                prev = current
                current = neighbor
                break
        if current == cycle[0]:
            break
        else:
            cycle.append(current)
 
    return cycle

"""
Finds a cycle in a graph with at least one vertex of degree 3

Args:
    G: a 2-d numpy array representing the graph as an adjacency matrix. 
       G must contain no vertices of degree 1 and at least one of degree 
       3 or greater

Returns:
    A list containing a=the vertices in the cycle.
"""
def find_deg3_cycle(G):
    
    predecessors = {}
    queue = deque()
    degrees = G.sum(1)
    
    for i, j in enumerate(degrees):
        if j > 2:
            queue.append(i)
            predecessors[i] = -1
            break
    
    while len(queue) > 0:
        current = queue.popleft()
        neighbors = [i for i, j in enumerate(G[current]) if j == 1]
        #print current

        for neighbor in neighbors:
            #print neighbor
            predecessors[neighbor] = current
            # follow paths degree 2 vertices as far as possible
            while(degrees[neighbor] < 3):
                # look at the neighbor's neighbors
                nns = [i for i,j in enumerate(G[neighbor]) if j == 1]
                for nn in nns:
                    if nn != predecessors[neighbor]:
                        predecessors[nn] = neighbor
                        neighbor = nn
                        break
            if neighbor in predecessors:
                return backtrace_cycle(predecessors, neighbor, current)
            else:
                queue.append(neighbor)
    return None

"""
Given a dict of predecessors from a search, walks pack to find a cycle

Args:
    preds: a dictionary of predecessors
    start: the beginning of the cycle found by the search
    end: the end of the cycle found by the search
"""
def backtrace_cycle(preds, start, end):
    #print preds
    #print start 
    #print end
    current = preds[end]
    cycle = [current]
    while current != start:
        parent = preds[current]
        cycle.append(parent)
        current = parent
    return cycle


def main():
    G1 = np.array([[0,1,0,1],
                   [1,0,1,0],
                   [0,1,0,1],
                   [1,0,1,0]])
    G2 = np.array([[0,1,1,0,0,0],
                   [1,0,1,0,0,0],
                   [1,1,0,1,0,0],
                   [0,0,1,0,1,1],
                   [0,0,0,1,0,1],
                   [0,0,0,1,1,0]])
    w1 = np.array([3,2,1,9])
    w2 = np.array([2,6,4,9,1,7])
    
    #print find_cycle(G1)
    #print find_cycle(G2)
    print feedback_vertex(G1,w1)
    print feedback_vertex(G2,w2)

if __name__ == '__main__':
    main()
