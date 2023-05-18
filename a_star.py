import heapq


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name, heuristic):
        self.vertices[name] = {}
        self.vertices[name]['heuristic'] = heuristic

    def add_edge(self, u, v, weight):
        if u not in self.vertices:
            raise ValueError(f"Vertex {u} not found in the graph.")
        if v not in self.vertices:
            raise ValueError(f"Vertex {v} not found in the graph.")
        self.vertices[u][v] = weight
        self.vertices[v][u] = weight


def astar(graph, start, goal):
    open_set = [(0, start)]  # Priority queue of nodes to be evaluated
    came_from = {}  # Dictionary to store the parent node of each node
    g_score = {vertex: float('inf') for vertex in graph.vertices}  # Cost from start along best known path
    g_score[start] = 0
    f_score = {vertex: float('inf') for vertex in graph.vertices}  # Estimated total cost from start to goal through y
    f_score[start] = graph.vertices[start]['heuristic']

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct the path from goal to start
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor in graph.vertices[current]:
            if neighbor == 'heuristic':
                continue

            tentative_g_score = g_score[current] + graph.vertices[current][neighbor]

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + graph.vertices[neighbor]['heuristic']

                # Add neighbor to the open set if it's not already there
                if neighbor not in [node[1] for node in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found


# Example usage:
g = Graph()
g.add_vertex('1', 1)
g.add_vertex('2', 1)
g.add_vertex('3', 8)
g.add_vertex('4', 7)
g.add_vertex('5', 6)
g.add_vertex('6', 1)
g.add_vertex('7', 1)
g.add_vertex('8', 3)
g.add_vertex('9', 2)
g.add_vertex('10', 1)

from laborator1 import read_from_file
edges = read_from_file("input.txt")
for edge in edges:
    g.add_edge(str(edge[0]), str(edge[1]), edge[1])
# g.add_edge('A', 'B', 1)
# g.add_edge('A', 'C', 3)
# g.add_edge('B', 'D', 2)
# g.add_edge('B', 'E', 4)
# g.add_edge('C', 'D', 1)
# g.add_edge('C', 'E', 7)
# g.add_edge('D', 'F', 5)
# g.add_edge('E', 'F', 3)

start_node = '1'
goal_node = '7'
path = astar(g, start_node, goal_node)
if path:
    print(f"Shortest path from {start_node} to {goal_node}: {' -> '.join(path)}")
else:
    print(f"No path found from {start_node} to {goal_node}.")


"""Graph class:

__init__(self): This method initializes the graph object. It initializes the vertices attribute as an empty dictionary to store the vertices and their edges.

add_vertex(self, name, heuristic): This method adds a vertex to the graph. It takes the name of the vertex and its heuristic value as parameters. It creates a new key in the vertices dictionary with the name as the key and an empty dictionary as the value. It also stores the heuristic value under the 'heuristic' key in the vertex's dictionary.

add_edge(self, u, v, weight): This method adds an edge between two vertices in the graph. It takes u and v as the names of the vertices and weight as the weight of the edge. It checks if both vertices exist in the vertices dictionary. If they do, it assigns the weight to the corresponding entries in the vertices' dictionaries, establishing a bidirectional connection.

astar function:

This function implements the A* algorithm to find the shortest path from the start node to the goal node in the given graph.

It initializes the open_set as a priority queue (implemented as a heap) to keep track of nodes to be evaluated. Each node in the queue is represented as a tuple (f_score, node), where f_score is the estimated total cost from start to goal through the given node, and node is the name of the node.

The came_from dictionary is used to store the parent node of each node in the shortest path.

The g_score dictionary stores the cost from the start node to each node along the best-known path, initialized with infinity for all nodes except the start node, which is initialized with a cost of 0.

The f_score dictionary stores the estimated total cost from the start node to the goal node through each node, initialized with infinity for all nodes except the start node, which is initialized with the heuristic value of the start node.

The algorithm starts by popping the node with the lowest f_score from the open_set. If the current node is the goal node, it reconstructs the shortest path from the goal to the start using the came_from dictionary and returns it.

Otherwise, it iterates through the neighbors of the current node. For each neighbor, it calculates the tentative g_score (the cost of the path from the start node to the neighbor through the current node). If the tentative g_score is lower than the current g_score for the neighbor, it updates the came_from, g_score, and f_score dictionaries for the neighbor and adds the neighbor to the open_set if it's not already there.

If the open_set is empty and the goal node has not been reached, the function returns None to indicate that no path was found.

The example usage demonstrates how to create a graph, add vertices with their heuristics, add edges between vertices, and then use the astar function to find the shortest path from the start node to the goal node in the graph. If a path is found, it prints the nodes in the shortest path. Otherwise, it informs the user that no path was found."""