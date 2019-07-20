class Vertex(object):
    def __init__(self, label):
        self.label = label

    def __str__(self):
     return self.label

class Graph(object):
    def __init__(self):
        self.adj_list = {}
        self.distances = {}
  
    def load_graph(self, number_of_vertices):
        #Fill graph with verticies, each labeled based on the value of i.
        for i in range(number_of_vertices):
            self.add_vertex(Vertex(i))

    def add_vertex(self, vertex: Vertex):
        self.adj_list[vertex] = []
        
    def insert_edge(self, vertex_A, vertex_B, dist):
        #Graph is undirected. This creates an edge for both directions. Distance is 
        #inserted in distances{} at (vertex_A, vertex_B) and (vertex_B, vertex_A).
        #A vertex is added to adj_list at both vertex_A and vertex_B.
        self.distances[(vertex_A, vertex_B)] = dist
        self.adj_list[vertex_A].append(vertex_B)
        
        self.distances[(vertex_B, vertex_A)] = dist
        self.adj_list[vertex_B].append(vertex_A)

    def return_vertex(self, loc_id):
        #Iterate through adj_list and return vertex if label is equal to loc_id.
        for v in self.adj_list:
            if(v.label == loc_id):
                return v
        return None

    def return_weight(self, vertex_A, vertex_B):
        return self.distances[(vertex_A, vertex_B)]

    def return_weight_with_id(self, id_A, id_B):
        #Allows weight to be returned by only providing the vertex label
        vertex_a = self.return_vertex(id_A)
        vertex_b = self.return_vertex(id_B)
        
        return self.distances[vertex_a, vertex_b]