from Vertex import Vertex

class Graph(object):
    def __init__(self):
        self.adj_list = {}
        self.distances = {}
        self.vertex_list = {}
  
    def load_graph(self, number_of_vertices):
        for i in range(number_of_vertices):
            self.add_vertex(Vertex(i), i)

    def add_vertex(self, vertex, id):
        self.adj_list[vertex] = []
        self.vertex_list[id] = vertex
        
    def add_directed_edge(self, from_vertex, to_vertex, dist):
        self.distances[(from_vertex, to_vertex)] = dist
        self.adj_list[from_vertex].append(to_vertex)
        
    def add_undirected_edge(self, vertex_a, vertex_b, dist):
        self.add_directed_edge(vertex_a, vertex_b, dist)
        self.add_directed_edge(vertex_b, vertex_a, dist)

    def return_vertex(self, label):
        return self.vertex_list[label]

    def return_weight(self, vertex_a, vertex_b):
        return self.distances[(vertex_a, vertex_b)]

    def return_weight_with_id(self, labelA, labelB):
        vertex_a = self.return_vertex(labelA)
        vertex_b = self.return_vertex(labelB)
        return self.distances[(vertex_a, vertex_b)]