from multiprocessing import Process
from multiprocessing.managers import BaseManager
import matplotlib.pyplot as plt
import networkx as nx
import random
import copy


class Graph:

    def __init__(self, edges_list=None, directed=True, weighted=True, graph=None):
        if graph:
            self.vertices = graph.vertices
            self.edges = graph.edges

        else:
            self.edges: list = copy.deepcopy(edges_list)
            self.vertices = {}
            self.directed = directed
            self.weighted = weighted

            for edge in edges_list:
                self.add_vertex(edge[0])
                self.add_vertex(edge[1])
                self.add_neighbour_to_vertex(edge[0], edge[1])
                if not self.directed:
                    self.edges.append([edge[1], edge[0], edge[2]])

    def get_vertices_obj(self):
        return self.vertices

    def add_neighbour_to_vertex(self, vertex, neighbour):

        if vertex not in self.vertices[neighbour]["in_neigh"]:
            self.vertices[neighbour]["in_neigh"].append(vertex)
        if neighbour not in self.vertices[vertex]["out_neigh"]:
            self.vertices[vertex]["out_neigh"].append(neighbour)

        if not self.directed:
            if vertex not in self.vertices[neighbour]["out_neigh"]:
                self.vertices[neighbour]["out_neigh"].append(vertex)
            if neighbour not in self.vertices[vertex]["in_neigh"]:
                self.vertices[vertex]["in_neigh"].append(neighbour)

    def delete_neighbour_from_vertex(self, vertex, neighbour):

        if neighbour in self.vertices[vertex]["in_neigh"]:
            self.vertices[vertex]["in_neigh"].remove(neighbour)
        if neighbour in self.vertices[vertex]["out_neigh"]:
            self.vertices[vertex]["out_neigh"].remove(neighbour)

    def get_vertices(self):
        return self.vertices.keys()

    def get_edges(self):
        return self.edges

    def add_edge(self, vertex1, vertex2, weight=None):

        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        self.add_neighbour_to_vertex(vertex1, vertex2)

        if [vertex1, vertex2, weight] not in self.edges:
            self.edges.append([vertex1, vertex2, weight])

        if not self.directed and [vertex2, vertex1, weight] not in self.edges:
            self.edges.append([vertex2, vertex1, weight])

    def add_vertex(self, vertex):
        if vertex not in self.vertices.keys():
            self.vertices[vertex] = {"in_neigh": [], "out_neigh": []}

    def get_no_vertices(self):
        return len(self.vertices.keys())

    def get_no_edges(self):
        return len(self.edges) if self.directed else int(len(self.edges)/2)

    def get_degrees_of_vertex(self, vertex):
        if vertex in self.vertices.keys():
            return len(self.vertices[vertex]["in_neigh"]), len(self.vertices[vertex]["out_neigh"])

        return None

    def get_neighbours_of_vertex(self, vertex):
        if vertex in self.vertices.keys():
            return self.vertices[vertex]["in_neigh"], self.vertices[vertex]["out_neigh"]

        return None

    def check_if_vertices_are_neighbours(self, vertex1, vertex2):

        if vertex1 in self.get_neighbours_of_vertex(vertex2)[0] or vertex1 in self.get_neighbours_of_vertex(vertex2)[
            1] or vertex2 in self.get_neighbours_of_vertex(vertex1)[0] or vertex2 in \
                self.get_neighbours_of_vertex(vertex1)[1]:
            return True
        return False

    def delete_vertex(self, vertex):

        if vertex in self.vertices.keys():
            in_neigh = copy.deepcopy(self.vertices[vertex]["in_neigh"])
            out_neigh = copy.deepcopy(self.vertices[vertex]["out_neigh"])

            for neighbour in in_neigh:
                self.delete_neighbour_from_vertex(neighbour, vertex)
                self.delete_edge([vertex, neighbour])
                self.delete_edge([neighbour, vertex])

            for neighbour in out_neigh:
                self.delete_neighbour_from_vertex(neighbour, vertex)
                self.delete_edge([vertex, neighbour])
                self.delete_edge([neighbour, vertex])

            self.vertices.pop(vertex)
            return vertex

        return None

    def delete_edge(self, edge):

        edges = copy.deepcopy(self.edges)
        for current_edge in edges:
            if current_edge[0] == edge[0] and current_edge[1] == edge[1]:
                self.edges.remove(current_edge)
                self.delete_neighbour_from_vertex(edge[0], edge[1])
                self.delete_neighbour_from_vertex(edge[1], edge[0])
                return current_edge

        return None

    def contract_edge(self, edge):

        deleted_edge = self.delete_edge([edge[0], edge[1]])
        if not self.directed:
            self.delete_edge([edge[1], edge[0]])

        in_neigh = copy.deepcopy(self.vertices[edge[1]]["in_neigh"])
        out_neigh = copy.deepcopy(self.vertices[edge[1]]["out_neigh"])

        for neighbour in in_neigh:
            if edge[0] != neighbour:
                self.add_neighbour_to_vertex(edge[0], neighbour)
            self.delete_edge([neighbour, edge[1]])
            if edge[0] != neighbour:
                self.add_edge(neighbour, edge[0], deleted_edge[2])

        for neighbour in out_neigh:
            if edge[0] != neighbour:
                self.add_neighbour_to_vertex(edge[0], neighbour)
            self.delete_edge([edge[1], neighbour])

            if edge[0] != neighbour:
                self.add_edge(edge[0], neighbour, deleted_edge[2])

        self.delete_vertex(edge[1])
        return edge if deleted_edge else None

    def draw_graph(self, specific_vertex=None):

        G = nx.Graph()
        pos = {}
        used_pos_x = []
        used_pos_y = []

        if specific_vertex is None:
            for vertex in self.vertices.keys():
                G.add_node(str(vertex))

                x = random.uniform(1, 10000000000)
                while x in used_pos_x:
                    x = round(random.uniform(1, 10000000000), 1)
                y = random.uniform(1, 10000000000)
                while y in used_pos_y:
                    y = round(random.rand(1, 10000000000), 1)

                pos[str(vertex)] = (x, y)
                used_pos_x.append(x)
                used_pos_y.append(y)

            for edge in self.edges:
                if not self.weighted:
                    G.add_edge(str(edge[0]), str(edge[1]))
                else:
                    G.add_edge(str(edge[0]), str(edge[1]), weight=str(edge[2]))

        elif specific_vertex in self.vertices.keys():
            G.add_node(str(specific_vertex))
            x = random.uniform(1, 10000000000)
            y = random.uniform(1, 10000000000)
            used_pos_x.append(x)
            used_pos_y.append(y)
            pos[str(specific_vertex)] = (x, y)

            for vertex in self.vertices[specific_vertex]["neighbours"]:
                G.add_node(str(vertex))
                G.add_edge(str(specific_vertex), str(vertex))

                while x in used_pos_x:
                    x = round(random.uniform(1, 10000000000), 1)
                while y in used_pos_y:
                    y = round(random.uniform(1, 10000000000), 1)

                pos[str(vertex)] = (x, y)
                used_pos_x.append(x)
                used_pos_y.append(y)

        else:
            print(f"Vertex {specific_vertex} does not exist")

        nx.draw(G, pos=pos, with_labels=True, node_color="red", node_size=500, font_color="white", font_size=20,
                font_family="Times New Roman", font_weight="bold", width=3, edge_color="black")
        plt.margins(0.2)
        plt.show()


def bfs(graph, start_node):
    visited = [False] * (len(graph.edges) + 1)
    queue = []
    result = []
    queue.append(start_node)
    visited[start_node] = True

    while queue:
        vertex = queue.pop(0)
        result.append(vertex)

        for node in graph.vertices[vertex]["out_neigh"]:
            if visited[node] is False:
                queue.append(node)
                visited[node] = True

            print(node)

    return result


class MyManager(BaseManager):
    pass


def delete_ingoing_edges(shared_memory: Graph, node, in_neigh):
    shared_memory.delete_edge([in_neigh, node])


def pbfs(graph, directed, weighted, start_node):

    visited = [False] * (len(graph.edges) + 1)
    queue = []
    result = []
    queue.append(start_node)
    visited[start_node] = True

    MyManager.register("Graph", Graph)
    with MyManager() as my_manager:
        shared_memory = my_manager.Graph(directed=directed, weighted=weighted, graph=graph)

        while queue:
            vertex = queue.pop(0)
            result.append(vertex)

            for node in shared_memory.get_vertices_obj()[vertex]["out_neigh"]:
                processes = list()

                for in_neigh in shared_memory.get_vertices_obj()[node]["in_neigh"]:
                    p = Process(target=delete_ingoing_edges, args=(shared_memory, node, in_neigh))
                    processes.append(p)

                for p in processes:
                    p.start()

                for p in processes:
                    p.join()

                if visited[node] is False:
                    queue.append(node)
                    visited[node] = True

                # print(shared_memory.get_edges())
                print(node)

    return result


def dfs(graph, vertex):

    def dfs_util(graph, vertex, visited, result):
        visited.add(vertex)
        result.append(vertex)

        for neighbour in graph.vertices[vertex]["out_neigh"]:
            if neighbour not in visited:
                dfs_util(graph, neighbour, visited, result)

        return result

    visited = set()
    result = []
    return dfs_util(graph, vertex, visited, result)


def read_from_file(name):
    with open(name) as file:
        lines = file.readlines()
        edges_list = []
        for line in lines:
            split_line = line.strip().split(' ')
            vertex1 = split_line[0]
            vertex2 = split_line[1]
            if len(split_line) > 2:
                edges_list.append([int(vertex1), int(vertex2), int(split_line[2])])
            else:
                edges_list.append([int(vertex1), int(vertex2), None])

    return edges_list


if __name__ == "__main__":
    run = input("run ?\n")

    if run == "fb":
        edges_list = read_from_file('facebook_combined.txt')
        graph = Graph(edges_list, directed=False, weighted=False)
        # print(bfs(graph, 0))
        from timeit import timeit
        print(timeit(lambda: pbfs(graph, True, False, 0), number=1))
        # print(pbfs(graph, True, False, 0))
        # print(graph.get_no_vertices())
        # print(graph.get_no_edges())
        # print(graph.get_degrees_of_vertex(6))
        # print(graph.get_neighbours_of_vertex(6))
        # print(graph.check_if_vertices_are_neighbours(0, 999))
        # graph.delete_edge([6, 0])
        # # graph.delete_vertex(6)
        # print(graph.get_neighbours_of_vertex(6))
        # print(graph.get_neighbours_of_vertex(319))
        # print(graph.contract_edge([6, 319]))
        # print(graph.get_neighbours_of_vertex(6))

    elif run == "test":
        edges_list = read_from_file('input.txt')
        graph = Graph(edges_list, directed=True, weighted=False)
        print(pbfs(graph, True, False, 1))
        # print(dfs(graph, 1))

# https://drive.google.com/drive/folders/1oMW20ug1mHug7HxvY_FJkOzpqL3hkw38