from collections import namedtuple


# class DirectedGraph:
   
#     def __init__(self,gdict=None):
#        if gdict is None:
#           gdict = []
#        self.gdict = gdict
 
#     def get_vertices(self):
#        return list(self.gdict.keys())
    
#     def get_edges(self):
#        return self.find_edges()
 
#     def find_edges(self):
#        edgename = []
#        for vrtx in self.gdict:
#           for nxtvrtx in self.gdict[vrtx]:
#              if {nxtvrtx, vrtx} not in edgename:
#                 edgename.append({vrtx, nxtvrtx})
#        return edgename
    
#     def add_vertex(self, vrtx):
#        if vrtx not in self.gdict:
#           self.gdict[vrtx] = []

#     def add_edge(self, edge):
#       edge = set(edge)
#       (vrtx1, vrtx2) = tuple(edge)
#       if vrtx1 in self.gdict:
#          self.gdict[vrtx1].append(vrtx2)
#       else:
#          self.gdict[vrtx1] = [vrtx2]


class UndirectedGraph:
   
   def __init__(self, edges_list=None):
      if edges_list is None:
         edges_list = []
      self.edges = edges_list

      self.vertices = {}
      for edge in edges_list:
         self.add_vertex(edge[0])
         self.add_vertex(edge[1])
         self.add_neighbour_to_vertex_and_increase_degrees(edge[0], edge[1])

   def add_neighbour_to_vertex_and_increase_degrees(self, neighbour, vertex):
      if vertex not in self.vertices[neighbour]["neighbours"]:
         self.vertices[neighbour]["neighbours"].append(vertex)
         self.vertices[neighbour]["degree"] += 1
      if neighbour not in self.vertices[vertex]["neighbours"]:
         self.vertices[vertex]["neighbours"].append(neighbour)
         self.vertices[vertex]["degree"] += 1

   def get_vertices(self):
      return self.vertices.keys()
   
   def get_edges(self):
      return self.edges
   
   def add_edge(self, vertex1, vertex2):
      self.add_vertex(vertex1)
      self.add_vertex(vertex2)
      
      if [vertex1, vertex2] not in self.edges:
         if vertex1 < vertex2:
            self.edges.append([vertex1, vertex2])
         else:
            self.edges.append([vertex2, vertex1])
            
         self.add_neighbour_to_vertex_and_increase_degrees(vertex1, vertex2)

   def add_vertex(self, vertex):
      if vertex not in self.vertices.keys():
         self.vertices[vertex] = {"neighbours": [],
                                      "degree": 0}

   def get_no_vertices(self):
      return len(self.vertices.keys())
   
   def get_no_edges(self):
      return len(self.edges)
   
   def get_degree_of_vertex(self, vertex):
      if vertex in self.vertices.keys():
         return self.vertices[vertex]["degree"]
      else:
         print(f"Vertex {vertex} does not exist")
   
   def get_neighbours_of_vertex(self, vertex):
      if vertex in self.vertices.keys():
         return self.vertices[vertex]["neighbours"]
      else:
         print(f"Vertex {vertex} does not exist")

   def check_if_vertices_are_neighbours(self, vertex1, vertex2):
      if vertex1 in self.vertices.keys() and vertex2 in self.vertices.keys() and ([vertex1, vertex2] in self.edges or [vertex2, vertex1] in self.edges):
         return True
      return False
   
   def delete_vertex(self, vertex):
      neighbours = self.vertices[vertex]["neighbours"]
      self.vertices.pop(vertex)

      for neighbor in neighbours:
         self.vertices[neighbor]["neighbours"].remove(vertex)
         self.vertices[neighbor]["degree"] -= 1
   
   def delete_edge(self, edge):
      if edge in self.edges:
         self.vertices[edge[0]]["neighbours"].remove(edge[1])
         self.vertices[edge[0]]["degree"] -= 1
         self.vertices[edge[1]]["neighbours"].remove(edge[0])
         self.vertices[edge[1]]["degree"] -= 1
         self.edges.remove(edge)
         
      else:
         print(f"Edge {edge} does not exist")

   def contract_edge(self, edge):
      if edge in self.edges:
         self.edges.remove(edge)
         vertex2_neighbours = self.vertices[edge[1]]["neighbours"]
         for vertex in vertex2_neighbours:
            if vertex not in self.vertices[edge[0]]["neighbours"] and vertex != edge[0]:
               self.vertices[edge[0]]["neighbours"].append(vertex)
               self.vertices[edge[0]]["degree"] += 1

               if edge[0] < vertex:
                  self.edges.append([edge[0], vertex])
               else:
                  self.edges.append([vertex, edge[0]])
            
            if [vertex, edge[1]] in self.edges and vertex != edge[0]:
               self.edges.remove([vertex, edge[1]])
               if edge[0] < vertex:
                  self.edges.append([edge[0], vertex])
               else:
                  self.edges.append([vertex, edge[0]])

            if [edge[1], vertex] in self.edges and vertex != edge[0]:
               self.edges.remove([edge[1], vertex])
               if edge[0] < vertex:
                  self.edges.append([edge[0], vertex])
               else:
                  self.edges.append([vertex, edge[0]])

         self.vertices[edge[0]]["neighbours"].remove(edge[1])
         self.vertices[edge[0]]["degree"] -= 1

      else:
         print(f"Edge {edge} does not exist")



with open('facebook_combined.txt') as file:
   lines = file.readlines()
   edges_list = []
   for line in lines:
      vertex1 = line.strip().split(' ')[0]
      vertex2 = line.strip().split(' ')[1]
      edges_list.append([int(vertex1), int(vertex2)])

graph = UndirectedGraph(edges_list)
# print(graph.get_vertices())
# print(graph.get_edges())
# print(graph.get_no_vertices())
# print(graph.get_no_edges())
print(graph.get_degree_of_vertex(3926))
print(graph.get_neighbours_of_vertex(3926))
print(graph.check_if_vertices_are_neighbours(0, 1))
graph.delete_edge([0, 1])
print(graph.check_if_vertices_are_neighbours(0, 1))
print(graph.check_if_vertices_are_neighbours(0, 2345))












# undirected_graph_elements = { 
#    "a" : ["b","c"],
#    "b" : ["a", "d"],
#    "c" : ["a", "d"],
#    "d" : ["e"],
#    "e" : ["d"]
# }
#
# g = DirectedGraph(undirected_graph_elements)
# g.add_edge({'a','e'})
# g.add_edge({'a','c'})
# g.add_vertex("f")
# print(g.get_vertices())
# print(g.get_edges())
