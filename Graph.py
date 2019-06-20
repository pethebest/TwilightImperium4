class Vertex:
    def __init__(self, hex_pos):
        self.hex_pos = hex_pos
        self.connectedTo = {}

    def add_neighbor(self, hex_pos):
        self.connectedTo[hex_pos] = True

    def __str__(self):
        return str(self.hex_pos) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def get_connections(self):
        return self.connectedTo.keys()

    def get_hex_pos(self):
        return self.hex_pos


class Graph:
    def __init__(self):
        self.vertexList = {}
        self.numVertices = 0

    def add_vertex(self, hex_pos):
        self.numVertices = self.numVertices + 1
        new_vertex = Vertex(hex_pos)
        self.vertexList[hex_pos] = new_vertex
        return new_vertex

    def get_vertex(self, hex_pos):
        if hex_pos in self.vertexList:
            return self.vertexList[hex_pos]
        else:
            return None

    def __contains__(self, hex_pos):
        return hex_pos in self.vertexList

    def add_edge(self, f, t):
        if f not in self.vertexList:
            nv = self.add_vertex(f)
        if t not in self.vertexList:
            nv = self.add_vertex(t)
        self.vertexList[f].add_neighbor(self.vertexList[t])

    def get_vertices(self):
        return self.vertexList.keys()

    def __iter__(self):
        return iter(self.vertexList.values())
