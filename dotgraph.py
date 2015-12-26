from collections import defaultdict

"""
Idea here; every "white" dot is a node, with an id

1) every pixel is a node
2) condense pixels to make the search graph a bit smaller (3x3 instead of 1x1)
3) run dijsktra from start to end and see how long it takes?

"""

# must be a square...
class Node(object):

    def __init__(self):

        self.id = None

        self.row = None
        self.col = None

        self._pixels = []

        self.graph = None

    @property
    def pixels(self):
        return self._pixels

    def add_pixels(self, pixels):
        #[(row, col), (row, col)]
        for pixel in pixels:
            self.add_pixel(pixel)

    def add_pixel(self, pixel):
        # (row, col)
        if pixel not in self._pixels:
            self._pixels.append(pixel)

    @property
    def boundary(self):
        """return top left and bottom right"""
        pass

    def get_neighbors(self):
        neighbors = set()
        for pixel in self.pixels:
            row, col = pixel
            # left
            left = (row , col - 1)
            right = (row, col + 1)
            up = (row - 1, col)
            down = (row + 1, col)
            neighbors.add(left)
            neighbors.add(right)
            neighbors.add(up)
            neighbors.add(down)

        return neighbors


class DotGraph(object):

    def __init__(self, array):
        self.array = array
        self.nodes = []
        self.edges = defaultdict(list)

        self._pixel_to_node = {}

    def add_node(self, node):
        self.nodes.append(node)
        self.reindex_node(node)

    def add_edge(self, from_node_id, to_node_id):
        if from_node_id == to_node_id:
            return

        if to_node_id not in self.edges[from_node_id]:
            self.edges[from_node_id].append(to_node_id)

        if from_node_id not in self.edges[to_node_id]:
            self.edges[to_node_id].append(from_node_id)

    def merge_node(self, hippo_id, food_id):
        hippo_node = self.node(hippo_id)
        food_node = self.node(food_id)

        # delete all food edges
        touching_nodes = self.edges[food_id]
        del self.edges[food_id]
        for node_id in touching_nodes:
            self.edges[node_id].remove(food_id)

        # add food's edges to hippo's set
        for node_id in touching_nodes:
            self.add_edge(hippo_id, node_id)

        # delete food node
        del self.nodes[food_id]

        # add food's pixel set to node's pixel set
        food_pixels = food_node.pixels
        hippo_node.add_pixels(food_pixels)
        self.reindex_node(hippo_node)

    # itorc sorta
    def node(self, id):
        return self.nodes[id]

    def pixel_to_node(self, pixel):
        return self._pixel_to_node.get(pixel)

    def reindex_node(self, node):
        for pixel in node.pixels:
            self._pixel_to_node[pixel] = node

class DotDetector(object):

    STATE_BLACK = 1
    STATE_WHITE = 2
    STATE_GRAY = 3

    def __init__(self, arr):
        self.array = arr

        l, r, t, b = self.find_edges()
        self.left_edge = l
        self.right_edge = r
        self.top_edge = t
        self.bottom_edge = b

    @staticmethod
    def _pixel_is_white(pixel):
        return pixel > 220

    @staticmethod
    def _pixel_is_black(pixel):
        return pixel < 20

    @staticmethod
    def _pixel_is_gray(pixel):
        return pixel < 200

    @property
    def width(self):
        return self.array.shape[1]

    @property
    def height(self):
        return self.array.shape[0]

    @staticmethod
    def _pixel_is(pixel, state):
        if state == DotDetector.STATE_BLACK:
            return DotDetector._pixel_is_black(pixel)
        if state == DotDetector.STATE_WHITE:
            return DotDetector._pixel_is_white(pixel)
        if state == DotDetector.STATE_GRAY:
            return DotDetector._pixel_is_gray(pixel)
        raise Exception("unknown pixel state")

    def find_edges(self):
        # left edge
        left_edge = 0
        for i in range(0, self.width):
            column = self.array[:, i]
            all_white = all([self._pixel_is_white(p) for p in column])
            if not all_white:
                left_edge = i
                break

        right_edge = self.width - 1
        for i in range(self.width - 1, 0, -1):
            column = self.array[:, i]
            all_white = all([self._pixel_is_white(p) for p in column])
            if not all_white:
                right_edge = i
                break

        top_edge = 0
        for i in range(0, self.height):
            row = self.array[i]
            all_white = all([self._pixel_is_white(p) for p in row])
            if not all_white:
                top_edge = i
                break

        bottom_edge = self.height - 1
        for i in range(self.height - 1, 0, -1):
            row = self.array[i]
            all_white = all([self._pixel_is_white(p) for p in row])
            if not all_white:
                bottom_edge = i
                break

        return left_edge, right_edge, top_edge, bottom_edge

    # in this model, and edge between pixels is defined as
    # both pixels are white and they're adjacent

    def generate_graph(self):
        start_row = self.top_edge
        start_col = self.left_edge

        rows, cols = self.array.shape
        end_row = self.bottom_edge
        end_col = self.right_edge

        node_counter = 0

        graph = DotGraph()
        print 'nodes'
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                try:
                    pixel = self.array[row][col]
                except IndexError:
                    continue

                if not self._pixel_is(pixel, self.STATE_WHITE):
                    continue

                node = Node()
                node.id = node_counter
                node.add_pixel((row, col))
                node.graph = graph
                node_counter += 1

                graph.add_node(node)

        # for each node, find adjacency
        print 'edges'
        for node in graph.nodes:
            for neighbor in node.get_neighbors():

                # if white, this is an edge
                if self._pixel_is(neighbor, self.STATE_WHITE):
                    neighbor_node = graph.pixel_to_node(neighbor)
                    if neighbor_node:
                        graph.add_edge(node.id, neighbor_node.id)

        return graph

