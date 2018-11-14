# 690AA Implementations
## Feedback Vertex Set
The feedback vertex set problem, as described on page 160 of 
Williamson-Shmoys, takes an undirected graph with non-negative weights
for each vertex. A minimum-cost set of vertices S should be found so that
if the vertices in S are removed the graph is disconnected.

### Implementation
The implementation is given in the file feedback.py, and particularly
in the method `feedback\_vertex(G, w)`. 

The method takes two arguments. `G` should be a *n*x*n* numpy array 
representing the graph as an adjacency matrix, where *n* is the number
of vertices in the graph. `w` should be a numpy array of length *n* containing
the weights for the vertices.

#### Example:
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

    print feedback_vertex(G1, w1) # [2]
    print feedback_vertex(G2, w2) # [0, 4]

## Shortest s-t path
The shortest s-t path problem is in P, but is instructive for the 
primal-dual method. This is a primal-dual approach to to problem, which
turns out to be equivalent to Dijkstra's algorithm.

### Implementation
The implementation is given in the file path.py, particularly in the method
`stpath(G, s, t)`. 

The method takes three arguments. `G` should be a *n*x*n* numpy array 
representing the graph as an adjacency matrix, where *n* is the number
of vertices in the graph. *G\_i,j* is the weight of the edge between *i* 
and *j*. If there is no edge between *i* and *j* this value should be 
`np.inf`. `s` and `t` should be the indices of the start and end vertices. 

#### Example:
    G = np.array([[np.inf, 10, 1, np.inf],
                  [10, np.inf, 3, 2],
                  [1, 3, np.inf, 6],
                  [np.inf, 2, 6, np.inf]])
    s = 0
    t = 3
    print stpath(G, s, t) # [0, 2, 1, 3]
