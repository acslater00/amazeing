from collections import defaultdict

class Node(object):
    def __init__(self):
        # node id, row, col
        self.id = None
        self.row = None
        self.col = None

        # parent
        self.graph = None

class MazeGraph(object):

    def __init__(self, row_count, col_count):

        # nodes
        self.nodes = []

        # these are directed
        self.edges = defaultdict(list)

        self.row_count = row_count
        self.col_count = col_count

    def rctoi(self, row, col):
        i = row * self.row_count + col
        return i

    def itorc(self, i):
        row, col = divmod(i, self.row_count)
        return row, col


    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, from_node_id, to_node_id):
        if to_node_id not in self.edges[from_node_id]:
            self.edges[from_node_id].append(to_node_id)

        if from_node_id not in self.edges[to_node_id]:
            self.edges[to_node_id].append(from_node_id)


# def dijsktra(graph, initial):
#   visited = {initial: 0}
#   path = {}

#   nodes = set(graph.nodes)

#   while nodes:
#     min_node = None
#     for node in nodes:
#       if node in visited:
#         if min_node is None:
#           min_node = node
#         elif visited[node] < visited[min_node]:
#           min_node = node

#     if min_node is None:
#       break

#     nodes.remove(min_node)
#     current_weight = visited[min_node]

#     for edge in graph.edges[min_node]:
#       weight = current_weight + graph.distance[(min_node, edge)]
#       if edge not in visited or weight < visited[edge]:
#         visited[edge] = weight
#         path[edge] = min_node

#   return visited, path
