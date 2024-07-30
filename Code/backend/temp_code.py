def BellmanFord(graph, V, E, src):
    maxsize = 0
    # Initialize distance of all vertices as infinite.
    dis = [maxsize] * V
 
    # initialize distance of source as 0
    dis[src] = 0
 
    # Relax all edges |V| - 1 times. A simple
    # shortest path from src to any other
    # vertex can have at-most |V| - 1 edges
    for i in range(V - 1):
        for j in range(E):
            if dis[graph[j][0]] + \
                   graph[j][2] < dis[graph[j][1]]:
                dis[graph[j][1]] = dis[graph[j][0]] + \
                                       graph[j][2]
 
    # check for negative-weight cycles.
    # The above step guarantees shortest
    # distances if graph doesn't contain
    # negative weight cycle. If we get a
    # shorter path, then there is a cycle.
    for i in range(E):
        x = graph[i][0]
        y = graph[i][1]
        weight = graph[i][2]
        if dis[x] != maxsize and dis[x] + \
                        weight < dis[y]:
            print("Graph contains negative weight cycle")
 
    print("Vertex Distance from Source")
    for i in range(V):
        print("%d\t\t%d" % (i, dis[i]))
 
# Driver Code
if __name__ == "__main__":
    V = 5 # Number of vertices in graph
    E = 8 # Number of edges in graph
 
    # Every edge has three values (u, v, w) where
    # the edge is from vertex u to v. And weight
    # of the edge is w.
    graph = [[0, 1, -1], [0, 2, 4], [1, 2, 3], 
             [1, 3, 2], [1, 4, 2], [3, 2, 5],
             [3, 1, 1], [4, 3, -3]]
    BellmanFord(graph, V, E, 0)
