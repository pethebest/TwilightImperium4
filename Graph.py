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

    def add_edge(self, hex_pos1, hex_pos2):
        if hex_pos1 not in self.vertexList:
            nv = self.add_vertex(hex_pos1)
        if hex_pos2 not in self.vertexList:
            nv = self.add_vertex(hex_pos2)
        self.vertexList[hex_pos1].add_neighbor(self.vertexList[hex_pos2])

    def get_vertices(self):
        return self.vertexList.keys()

    def __iter__(self):
        return iter(self.vertexList.values())

    def breadth_first_search(self, hex_pos, max_depth):
        """
        :param hex_pos: is a starting hex (tuple)
        :param max_depth: is an integer that represents the maximum depth we look at, so for a depth of 1, you get the
        first neighbors, 2, you get the next neighbors etc... This is similar BUT NOT EQUIVALENT TO DISTANCE, as it is
        possible to travel back to our starting point with a distance of 2 for instance, in fact it represents the
        shortest path to a place
        :return: an array of tuple, the first part of each tuple is an accessible hex, and the second part is its depth
        """
        if isinstance(hex_pos, Vertex):
            hex_pos = hex_pos.get_hex_pos()
        visited, queue = set(), [(hex_pos, 0)]
        while queue:
            vertex, depth = queue.pop(0)
            if depth == max_depth+1:
                break
            if vertex not in visited:
                visited.add((vertex, depth))
                list_of_neighbors = set([(v.get_hex_pos(), depth+1) for v in self.vertexList[vertex].get_connections()])
                queue.extend(list_of_neighbors - visited)
        return visited


