import matplotlib.pyplot as plt
import networkx as nx
import random


class Graph:

    def __init__(self, edges_list, directed=True, weighted=True):
        self.edges = edges_list
        self.vertices = {}
        self.directed = directed
        self.weighted = weighted

        for edge in edges_list:
            self.add_vertex(edge[0])
            self.add_vertex(edge[1])
            self.add_neighbour_to_vertex(edge[1], edge[0])

    def add_neighbour_to_vertex(self, neighbour, vertex):
        if neighbour not in self.vertices[vertex]["neighbours"]:
            self.vertices[vertex]["neighbours"].append(neighbour)

        if not self.directed and vertex not in self.vertices[neighbour]["neighbours"]:
            self.vertices[neighbour]["neighbours"].append(vertex)

    def get_vertices(self):
        return self.vertices.keys()

    def get_edges(self):
        return self.edges

    def add_edge(self, vertex1, vertex2, weight=None):
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)

        if not self.weighted and [vertex1, vertex2] not in self.edges:
            if vertex1 < vertex2:
                self.edges.append([vertex1, vertex2])

            else:
                self.edges.append([vertex2, vertex1])

            self.add_neighbour_to_vertex(vertex2, vertex1)

        elif self.weighted and [vertex1, vertex2, weight] not in self.edges:
            if vertex1 < vertex2:
                self.edges.append([vertex1, vertex2, weight])
            else:
                self.edges.append([vertex2, vertex1, weight])

            self.add_neighbour_to_vertex(vertex2, vertex1)

    def add_vertex(self, vertex):
        if vertex not in self.vertices.keys():
            self.vertices[vertex] = {"neighbours": [], "visited": False}

    def get_no_vertices(self):
        return len(self.vertices.keys())

    def get_no_edges(self):
        return len(self.edges)

    def get_degree_of_vertex(self, vertex):
        if vertex in self.vertices.keys():
            return len(self.vertices[vertex]["neighbours"])
        else:
            print(f"Vertex {vertex} does not exist")

    def get_neighbours_of_vertex(self, vertex):
        if vertex in self.vertices.keys():
            return self.vertices[vertex]["neighbours"]
        else:
            print(f"Vertex {vertex} does not exist")

    def check_if_vertices_are_neighbours(self, vertex1, vertex2):
        if vertex1 in self.vertices.keys() and vertex2 in self.vertices.keys() and (
                [vertex1, vertex2] in self.edges or [vertex2, vertex1] in self.edges):
            return True
        return False

    def delete_vertex(self, vertex):
        if vertex in self.vertices.keys():
            neighbours = self.vertices[vertex]["neighbours"]
            self.vertices.pop(vertex)

            for neighbor in neighbours:
                if vertex in self.vertices[neighbor]["neighbours"]:
                    self.vertices[neighbor]["neighbours"].remove(vertex)

            for neighbour in neighbours:
                if [neighbour, vertex] in self.edges:
                    self.edges.remove([neighbour, vertex])
                elif [vertex, neighbour] in self.edges:
                    self.edges.remove([vertex, neighbour])

            print(f"Vertex {vertex} was deleted")

        else:
            print(f"Vertex {vertex} does not exist")

    def delete_edge(self, edge):
        if edge in self.edges:
            self.vertices[edge[0]]["neighbours"].remove(edge[1])
            if not self.directed:
                self.vertices[edge[1]]["neighbours"].remove(edge[0])
            self.edges.remove(edge)
            print(f"Edge {edge} was deleted")

        else:
            print(f"Edge {edge} does not exist")

    def contract_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            vertex2_neighbours = self.vertices[edge[1]]["neighbours"]
            for vertex in vertex2_neighbours:

                # self.vertices[vertex]["neighbours"].remove(edge[1])

                if vertex not in self.vertices[edge[0]]["neighbours"] and vertex != edge[0]:
                    self.vertices[edge[0]]["neighbours"].append(vertex)

                    if edge[0] < vertex:
                        self.edges.append([edge[0], vertex])
                    else:
                        self.edges.append([vertex, edge[0]])

                if [vertex, edge[1]] in self.edges and vertex != edge[0]:
                    self.edges.remove([vertex, edge[1]])

                if [edge[1], vertex] in self.edges and vertex != edge[0]:
                    self.edges.remove([edge[1], vertex])

            self.vertices.pop(edge[1])

            print(f"Edge {edge} was contracted. Vertex {edge[1]} does not exist anymore")

        else:
            print(f"Edge {edge} does not exist")

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
                G.add_edge(str(edge[0]), str(edge[1]))

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

        nx.draw(G, pos=pos, with_labels=True, node_color="red", node_size=1000, font_color="white", font_size=20,
                font_family="Times New Roman", font_weight="bold", width=3, edge_color="black")
        plt.margins(0.2)
        plt.show()


with open('facebook_combined.txt') as file:
    lines = file.readlines()
    edges_list = []
    for line in lines:
        split_line = line.strip().split(' ')
        vertex1 = split_line[0]
        vertex2 = split_line[1]
        if len(split_line) > 2:
            edges_list.append([int(vertex1), int(vertex2), int(split_line[2])])
        else:
            edges_list.append([int(vertex1), int(vertex2)])

graph = Graph(edges_list, directed=True, weighted=False)
print("get_vertices()", graph.get_vertices())
print("get_edges()", graph.get_edges())
print("get_no_vertices()", graph.get_no_vertices())
print("get_no_edges()", graph.get_no_edges())
print("get_degree_of_vertex(3926)", graph.get_degree_of_vertex(3926))
print("get_neighbours_of_vertex(3926)", graph.get_neighbours_of_vertex(3926))
print("check_if_vertices_are_neighbours(0, 1)", graph.check_if_vertices_are_neighbours(0, 1))
print("check_if_vertices_are_neighbours(1912, 2603)", graph.check_if_vertices_are_neighbours(1912, 2603))
print(graph.get_neighbours_of_vertex(6))
print(graph.get_neighbours_of_vertex(319))
graph.contract_edge([6, 319])
print(graph.get_neighbours_of_vertex(6))
print(graph.get_neighbours_of_vertex(319))
graph.delete_edge([1912, 2603])
graph.delete_vertex(2)
print("check_if_vertices_are_neighbours(0, 1)", graph.check_if_vertices_are_neighbours(0, 1))
print("check_if_vertices_are_neighbours(1912, 2603)", graph.check_if_vertices_are_neighbours(1912, 2603))
graph.draw_graph()
