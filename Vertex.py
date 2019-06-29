class Vertex(object):
    def __init__(self, label):
        self.label = label
        self.distance = float('inf')
        self.pred_vertex = None

    def __str__(self):
     return self.label

