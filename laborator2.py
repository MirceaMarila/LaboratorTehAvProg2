from collections import namedtuple
import matplotlib.pyplot as plt
import networkx as nx
import random


Edge = namedtuple('Edge', ['frm', 'to', 'weight'])
Vertex = namedtuple('Vertex', ['name', 'nlist', 'parent', 'visited'])


class Graph:
   
   def __init__(self, edges_list=None, directed=True, weighted=True):

      self.edges = []
      self.vertices = []
      self.directed = directed
      self.weighted = weighted

      for edge in edges_list:
         self.edges.append(Edge(edge[0], edge[1], edge[2] if weighted else None))

      for edge in self.edges:
         self.add_vertex(edge.frm)
         self.add_vertex(edge.to)
         self.add_neighbour_to_vertex(edge.frm, edge.to)
         if not self.directed:
            self.add_neighbour_to_vertex(edge.to, edge.frm)

   def get_vertex_by_name(self, name):
      for vertex in self.vertices:
         if vertex.name == name:
            return vertex
         
      print(f"Vertex {name} does not exist")
      return None
   
   def get_edge_by_name(self, name):
      for edge in self.edges:
         if edge.frm == name[0] and edge.to == name[1]:
            return edge
         
      print(f"Edge {name} does not exist")
      return None

   def add_neighbour_to_vertex(self, neighbour_name, vertex_name):
      if vertex_name not in self.get_vertices():
         print(f"Vertex {vertex_name} does not exist")

      if neighbour_name not in self.get_vertices():
         print(f"Vertex {neighbour_name} does not exist")

      vertex = self.get_vertex_by_name(vertex_name)

      if neighbour_name not in vertex.nlist:
         vertex.nlist.append(neighbour_name)

   def get_vertices(self):
      return [vertex.name for vertex in self.vertices]
   
   def get_edges(self):
      return [[edge.frm, edge.to] for edge in self.edges]
   
   def get_weight_of_edge(self, edge_name):
      if self.weighted:
         for edge in self.edges:
            if edge.frm == edge_name[0] and edge.to == edge_name[1]:
               return edge.weight

         else:
            print(f"Edge {edge_name} does not exist")
            return None
   
   def add_edge(self, vertex1_name, vertex2_name, weight=None):
      self.add_vertex(vertex1_name)
      self.add_vertex(vertex2_name)
      if self.weighted and weight is None:
         weight = 0
      
      if [vertex1_name, vertex2_name] not in self.get_edges() and [vertex2_name, vertex1_name] not in self.get_edges():
         if vertex1_name < vertex2_name:
            self.edges.append(Edge(vertex1_name, vertex2_name, weight))
         else:
            self.edges.append(Edge(vertex2_name, vertex1_name, weight))
            
         self.add_neighbour_to_vertex(vertex1_name, vertex2_name)
         if not self.directed:
            self.add_neighbour_to_vertex(vertex2_name, vertex1_name)

   def add_vertex(self, vertex_name):
      if vertex_name not in self.get_vertices():
         self.vertices.append(Vertex(vertex_name, [], None, False))

   def get_no_vertices(self):
      return len(self.vertices)
   
   def get_no_edges(self):
      return len(self.edges)
   
   def get_degree_of_vertex(self, vertex_name):
      if vertex_name in self.get_vertices():
         return len(self.get_vertex_by_name(vertex_name).nlist)
      else:
         print(f"Vertex {vertex_name} does not exist")
   
   def get_neighbours_of_vertex(self, vertex_name):
      if vertex_name in self.get_vertices():
         return self.get_vertex_by_name(vertex_name).nlist
      else:
         print(f"Vertex {vertex_name} does not exist")

   def check_if_vertices_are_neighbours(self, vertex1_name, vertex2_name):
      if vertex1_name in self.get_neighbours_of_vertex(vertex2_name) or vertex2_name in self.get_neighbours_of_vertex(vertex1_name):
         return True
      return False
   
   def delete_vertex(self, vertex_name):
      if vertex_name in self.get_vertices():
         vertex = self.get_vertex_by_name(vertex_name)
         neighbours = vertex.nlist
         self.vertices.pop(vertex)

         for neighbor_name in neighbours:
            neighbor = self.get_neighbor_by_name(neighbor_name)
            neighbor.nlist.remove(vertex_name)
      
      else:
         print(f"Vertex {vertex_name} does not exist")
   
   def delete_edge(self, edge_name):
      if edge_name in self.get_edges():
         self.get_vertex_by_name(edge_name[0]).nlist.remove(edge_name[1])

         if not self.directed:
            self.get_vertex_by_name(edge_name[1]).nlist.remove(edge_name[0])

         self.edges.remove(self.get_edge_by_name(edge_name))
         print(f"Edge {edge_name} was deleted")
         
      else:
         print(f"Edge {edge_name} does not exist")

   def contract_edge(self, edge_name):
      if edge_name in self.get_edges():
         self.edges.remove(self.get_edge_by_name(edge_name))
         vertex2_neighbours = self.get_vertex_by_name(edge_name[1]).nlist
         for vertex_name in vertex2_neighbours:
            if vertex_name not in self.get_vertex_by_name(edge_name[0]).nlist and vertex_name != edge_name[0]:
               self.get_vertex_by_name(edge_name[0]).nlist.append(vertex_name)

               if edge_name[0] < vertex_name:
                  self.edges.append(Edge(edge_name[0], vertex_name, edge_name[2] if self.weighted else None))
               else:
                  self.edges.append(Edge(vertex_name, edge_name[0], edge_name[2] if self.weighted else None))
            
            if [vertex_name, edge_name[1]] in self.get_edges() and vertex_name != edge_name[0]:
               self.edges.remove(self.get_edge_by_name([vertex_name, edge_name[1]]))

            if [edge_name[1], vertex_name] in self.get_edges() and vertex_name != edge_name[0]:
               self.edges.remove(self.get_edge_by_name([edge_name[1], vertex_name]))

         self.get_vertex_by_name(edge_name[0]).nlist.remove(edge_name[1])
         self.vertices.pop(self.get_vertex_by_name(edge_name[1]))

      else:
         print(f"Edge {edge_name} does not exist")

   def draw_graph(self, specific_vertex=None):
      G=nx.Graph()
      pos = {}
      used_pos_x = []
      used_pos_y = []

      if specific_vertex is None:
         for vertex in self.get_vertices():
            G.add_node(str(vertex))

            x = random.uniform(1, 10000000000)
            while x in used_pos_x:
               x = round( random.uniform(1, 10000000000), 1)
            y = random.uniform(1, 10000000000)
            while y in used_pos_y:
               y = round( random.rand(1, 10000000000), 1)

            pos[str(vertex)] = (x, y)
            used_pos_x.append(x)
            used_pos_y.append(y)


         for edge in self.get_edges:
            G.add_edge(str(edge[0]), str(edge[1]))

      elif specific_vertex in self.get_vertices():
         G.add_node(str(specific_vertex))
         x = random.uniform(1, 10000000000)
         y = random.uniform(1, 10000000000)
         used_pos_x.append(x)
         used_pos_y.append(y)
         pos[str(specific_vertex)] = (x, y)

         for vertex in self.get_vertex_by_name(specific_vertex).nlist:
            G.add_node(str(vertex))
            G.add_edge(str(specific_vertex), str(vertex))

            while x in used_pos_x:
               x = round( random.uniform(1, 10000000000), 1)
            while y in used_pos_y:
               y = round( random.uniform(1, 10000000000), 1)

            pos[str(vertex)] = (x, y)
            used_pos_x.append(x)
            used_pos_y.append(y)
      
      else:
         print(f"Vertex {specific_vertex} does not exist")

      
      nx.draw(G,pos=pos,with_labels=True,node_color="red",node_size=1000,font_color="white",font_size=20,font_family="Times New Roman", font_weight="bold",width=3,edge_color="black")
      plt.margins(0.2)
      plt.show()


if __name__ == "__main__":
   # with open('input.txt') as file:
   with open('facebook_combined.txt') as file:
      lines = file.readlines()
      edges_list = []
      for line in lines:
         vertex1 = line.strip().split(' ')[0]
         vertex2 = line.strip().split(' ')[1]
         if len(line.strip().split(' ')) > 2:
            weight = int(line.strip().split(' ')[2])
         else:
            weight = None
         edges_list.append([int(vertex1), int(vertex2), weight])

   graph = Graph(edges_list, directed=True, weighted=True)
   print("get_vertices()", graph.get_vertices())
   print("get_edges()", graph.get_edges())
   print("get_no_vertices()", graph.get_no_vertices())
   print("get_no_edges()", graph.get_no_edges())
   print("get_degree_of_vertex(3926)", graph.get_degree_of_vertex(3926))
   print("get_neighbours_of_vertex(3926)", graph.get_neighbours_of_vertex(3926))
   print("check_if_vertices_are_neighbours(0, 1)", graph.check_if_vertices_are_neighbours(0, 1))
   graph.contract_edge([0, 1])
   print("check_if_vertices_are_neighbours(0, 1)", graph.check_if_vertices_are_neighbours(0, 1))
   print("check_if_vertices_are_neighbours(0, 2345)", graph.check_if_vertices_are_neighbours(0, 2345))
   graph.draw_graph()
