def dijsktra(graph, initial, terminal=None):
    visited = {initial: 0}
    path = {}

    nodes = set([n.id for n in graph.nodes])

    ct = 0
    while nodes:
        ct += 1
        if ct % 100 == 0:
            print ct
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            weight = current_weight + 1
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path

def min_path(graph, initial, terminal):
    node_distance, path = dijsktra(graph, initial)

    distance = node_distance[terminal]
    backpath = [terminal]
    end = terminal
    try:
        while end != initial:
            end = path[end]
            backpath.append(end)
        path = list(reversed(backpath))
    except KeyError:
        path = None

    return distance, path


### faster dijstra?


from heapq import *

def min_path2(graph, initial, terminal):

    # cost, start, path?
    q = [(0, initial, ())]
    visited = set()
    path = {}


    while q:
        cost, v1, path = heappop(q)

        if v1 not in visited:
            visited.add(v1)
            path = (v1,) + path

            if v1 == terminal:
                return (cost, path)

            for v2 in graph.edges[v1]:
                if v2 not in visited:
                    heappush(q, (cost + 1, v2, path))

