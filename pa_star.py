import heapq
from multiprocessing import Pool, cpu_count

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name, heuristic):
        self.vertices[name] = {'heuristic': heuristic}

    def add_edge(self, u, v, weight):
        if u not in self.vertices:
            raise ValueError(f"Vertex {u} not found in the graph.")
        if v not in self.vertices:
            raise ValueError(f"Vertex {v} not found in the graph.")
        self.vertices[u][v] = weight
        self.vertices[v][u] = weight

def process_neighbor(args):
    neighbor, current, graph, g_score, f_score, came_from = args
    tentative_g_score = g_score[current] + graph.vertices[current][neighbor]

    if tentative_g_score < g_score[neighbor]:
        came_from[neighbor] = current
        g_score[neighbor] = tentative_g_score
        f_score[neighbor] = tentative_g_score + graph.vertices[neighbor]['heuristic']

        return (f_score[neighbor], neighbor)

    return None

def astar(graph, start, goal):
    open_set = [(0, start)]  # Priority queue of nodes to be evaluated
    came_from = {}  # Dictionary to store the parent node of each node
    g_score = {vertex: float('inf') for vertex in graph.vertices}  # Cost from start along best known path
    g_score[start] = 0
    f_score = {vertex: float('inf') for vertex in graph.vertices}  # Estimated total cost from start to goal through y
    f_score[start] = graph.vertices[start]['heuristic']

    pool = Pool(cpu_count())

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

        neighbors = list(graph.vertices[current].keys())
        args_list = [(neighbor, current, graph, g_score, f_score, came_from) for neighbor in neighbors if neighbor != 'heuristic']
        results = pool.map(process_neighbor, args_list)

        for result in results:
            if result is not None:
                heapq.heappush(open_set, result)

    return None  # No path found


if __name__ == '__main__':
    # Example usage:
    g = Graph()
    g.add_vertex('A', 5)
    g.add_vertex('B', 4)
    g.add_vertex('C', 2)
    g.add_vertex('D', 3)
    g.add_vertex('E', 1)
    g.add_vertex('F', 0)

    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 3)
    g.add_edge('B', 'D', 2)
    g.add_edge('B', 'E', 4)
    g.add_edge('C', 'D', 1)
    g.add_edge('C', 'E', 7)
    g.add_edge('D', 'F', 5)
    g.add_edge('E', 'F', 3)

    start_node = 'A'
    goal_node = 'F'
    path = astar(g, start_node, goal_node)
    if path:
        print(f"Shortest path from {start_node} to {goal_node}: {' -> '.join(path)}")
    else:
        print(f"No path found from {start_node} to {goal_node}.")


