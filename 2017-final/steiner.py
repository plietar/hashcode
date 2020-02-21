import math


parent = dict()
rank = dict()

def make_set(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0

def find(vertice):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice])
    return parent[vertice]

def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]: rank[root2] += 1

def kruskal(graph):
    for vertice in graph['vertices']:
        make_set(vertice)

    minimum_spanning_tree = set()
    edges = list(graph['edges'])
    edges.sort()
    for edge in edges:
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            minimum_spanning_tree.add(edge)
    return minimum_spanning_tree

def distance(r, r2):
    (x, y), (x2, y2) = r, r2
    return max(abs(x - x2), abs(y - y2))

def make_graph(routers):
    n = len(routers)
    e = set()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = distance(routers[i], routers[j])
            e.add((d, routers[i], routers[j]))
    return {'vertices': routers, 'edges': e}
    

def process_routers(routers):
    mst = kruskal(make_graph(routers))
    size = 0
    for (d, _, _) in mst:
        size += int(math.sqrt(d))
    return mst, size







#graph = {
#        'vertices': ['A', 'B', 'C', 'D', 'E', 'F'],
#        'edges': set([
#            (1, 'A', 'B'),
#            (5, 'A', 'C'),
#            (3, 'A', 'D'),
#            (4, 'B', 'C'),
#            (2, 'B', 'D'),
#            (1, 'C', 'D'),
#            ])
#        }
#minimum_spanning_tree = set([
#            (1, 'A', 'B'),
#            (2, 'B', 'D'),
#            (1, 'C', 'D'),
#            ])
#assert kruskal(graph) == minimum_spanning_tree


