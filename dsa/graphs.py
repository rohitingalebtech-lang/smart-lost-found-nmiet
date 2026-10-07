"""
GRAPH DATA STRUCTURES & ALGORITHMS
Smart Lost & Found Management System
NMIET B.Tech AI & Data Science

Covered:
1. Graph Representation
2. Breadth First Search (BFS)
3. Depth First Search (DFS)
4. Dijkstra's Shortest Path
5. Prim's Minimum Spanning Tree
6. Kruskal's Minimum Spanning Tree
"""


# ============================================================
# 1. GRAPH REPRESENTATION
# ============================================================

class CampusGraph:

    def __init__(self):
        self.graph = {}

    def add_location(self, location):
        if location not in self.graph:
            self.graph[location] = []

    def add_connection(self, location1, location2, distance):
        self.add_location(location1)
        self.add_location(location2)

        self.graph[location1].append(
            (location2, distance)
        )

        self.graph[location2].append(
            (location1, distance)
        )

    def display(self):
        for location, connections in self.graph.items():

            print(f"{location}:")

            for destination, distance in connections:
                print(
                    f"  -> {destination} ({distance} m)"
                )


# ============================================================
# 2. BREADTH FIRST SEARCH (BFS)
# ============================================================

from collections import deque


def bfs(graph, start):

    visited = set()
    queue = deque([start])
    result = []

    visited.add(start)

    while queue:

        current = queue.popleft()
        result.append(current)

        for neighbour, _ in graph.get(current, []):

            if neighbour not in visited:

                visited.add(neighbour)
                queue.append(neighbour)

    return result


# ============================================================
# 3. DEPTH FIRST SEARCH (DFS)
# ============================================================

def dfs(graph, start):

    visited = set()
    result = []

    def explore(location):

        visited.add(location)
        result.append(location)

        for neighbour, _ in graph.get(location, []):

            if neighbour not in visited:
                explore(neighbour)

    explore(start)

    return result


# ============================================================
# 4. DIJKSTRA'S SHORTEST PATH
# ============================================================

def dijkstra(graph, start):

    distances = {}

    previous = {}

    unvisited = set(graph.keys())

    for location in graph:
        distances[location] = float("inf")
        previous[location] = None

    if start not in graph:
        return distances, previous

    distances[start] = 0

    while unvisited:

        current = min(
            unvisited,
            key=lambda location: distances[location]
        )

        if distances[current] == float("inf"):
            break

        unvisited.remove(current)

        for neighbour, distance in graph[current]:

            new_distance = (
                distances[current] + distance
            )

            if new_distance < distances[neighbour]:

                distances[neighbour] = new_distance
                previous[neighbour] = current

    return distances, previous


def shortest_path(graph, start, destination):

    distances, previous = dijkstra(
        graph,
        start
    )

    if destination not in distances:
        return [], float("inf")

    if distances[destination] == float("inf"):
        return [], float("inf")

    path = []
    current = destination

    while current is not None:

        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[destination]


# ============================================================
# 5. PRIM'S MINIMUM SPANNING TREE
# ============================================================

def prim_mst(graph, start):

    if start not in graph:
        return [], 0

    visited = set()
    edges = []
    mst = []
    total_weight = 0

    visited.add(start)

    for neighbour, weight in graph[start]:

        edges.append(
            (weight, start, neighbour)
        )

    while edges:

        edges.sort(key=lambda edge: edge[0])

        weight, source, destination = edges.pop(0)

        if destination in visited:
            continue

        visited.add(destination)

        mst.append(
            (source, destination, weight)
        )

        total_weight += weight

        for neighbour, next_weight in graph[destination]:

            if neighbour not in visited:

                edges.append(
                    (
                        next_weight,
                        destination,
                        neighbour
                    )
                )

    return mst, total_weight


# ============================================================
# 6. DISJOINT SET FOR KRUSKAL'S ALGORITHM
# ============================================================

class DisjointSet:

    def __init__(self, vertices):

        self.parent = {
            vertex: vertex
            for vertex in vertices
        }

        self.rank = {
            vertex: 0
            for vertex in vertices
        }

    def find(self, vertex):

        if self.parent[vertex] != vertex:

            self.parent[vertex] = self.find(
                self.parent[vertex]
            )

        return self.parent[vertex]

    def union(self, vertex1, vertex2):

        root1 = self.find(vertex1)
        root2 = self.find(vertex2)

        if root1 == root2:
            return False

        if self.rank[root1] < self.rank[root2]:

            self.parent[root1] = root2

        elif self.rank[root1] > self.rank[root2]:

            self.parent[root2] = root1

        else:

            self.parent[root2] = root1
            self.rank[root1] += 1

        return True


# ============================================================
# 7. KRUSKAL'S MINIMUM SPANNING TREE
# ============================================================

def kruskal_mst(graph):

    edges = []
    vertices = set(graph.keys())

    for source in graph:

        for destination, weight in graph[source]:

            if (destination, source, weight) not in edges:

                edges.append(
                    (
                        weight,
                        source,
                        destination
                    )
                )

    edges.sort(key=lambda edge: edge[0])

    disjoint_set = DisjointSet(vertices)

    mst = []
    total_weight = 0

    for weight, source, destination in edges:

        if disjoint_set.union(
            source,
            destination
        ):

            mst.append(
                (
                    source,
                    destination,
                    weight
                )
            )

            total_weight += weight

    return mst, total_weight


# ============================================================
# NMIET CAMPUS SAMPLE GRAPH
# ============================================================

def create_nmiet_campus_graph():

    campus = CampusGraph()

    campus.add_connection(
        "Main Gate",
        "Administrative Office",
        120
    )

    campus.add_connection(
        "Main Gate",
        "Canteen",
        180
    )

    campus.add_connection(
        "Administrative Office",
        "Library",
        100
    )

    campus.add_connection(
        "Administrative Office",
        "Classroom Block",
        150
    )

    campus.add_connection(
        "Library",
        "Laboratory",
        90
    )

    campus.add_connection(
        "Library",
        "Canteen",
        140
    )

    campus.add_connection(
        "Classroom Block",
        "Laboratory",
        110
    )

    campus.add_connection(
        "Classroom Block",
        "Playground",
        200
    )

    campus.add_connection(
        "Laboratory",
        "Workshop",
        130
    )

    campus.add_connection(
        "Canteen",
        "Playground",
        160
    )

    return campus


# ============================================================
# TEST GRAPH ALGORITHMS
# ============================================================

def test_graph_algorithms():

    print("=" * 65)
    print("NMIET SMART LOST & FOUND - GRAPH ALGORITHM TEST")
    print("=" * 65)

    campus = create_nmiet_campus_graph()

    # --------------------------------------------------------
    # Graph Representation
    # --------------------------------------------------------

    print("\n--- GRAPH REPRESENTATION ---")

    campus.display()

    # --------------------------------------------------------
    # BFS
    # --------------------------------------------------------

    print("\n--- BREADTH FIRST SEARCH (BFS) ---")

    bfs_result = bfs(
        campus.graph,
        "Main Gate"
    )

    print(bfs_result)

    # --------------------------------------------------------
    # DFS
    # --------------------------------------------------------

    print("\n--- DEPTH FIRST SEARCH (DFS) ---")

    dfs_result = dfs(
        campus.graph,
        "Main Gate"
    )

    print(dfs_result)

    # --------------------------------------------------------
    # Dijkstra
    # --------------------------------------------------------

    print("\n--- DIJKSTRA SHORTEST PATH ---")

    path, distance = shortest_path(
        campus.graph,
        "Main Gate",
        "Workshop"
    )

    print("Path:")
    print(" -> ".join(path))

    print(f"Shortest Distance: {distance} meters")

    # --------------------------------------------------------
    # Prim
    # --------------------------------------------------------

    print("\n--- PRIM'S MINIMUM SPANNING TREE ---")

    prim_result, prim_weight = prim_mst(
        campus.graph,
        "Main Gate"
    )

    for source, destination, weight in prim_result:

        print(
            f"{source} -> {destination} = {weight} m"
        )

    print(
        f"Total MST Weight: {prim_weight} meters"
    )

    # --------------------------------------------------------
    # Kruskal
    # --------------------------------------------------------

    print("\n--- KRUSKAL'S MINIMUM SPANNING TREE ---")

    kruskal_result, kruskal_weight = kruskal_mst(
        campus.graph
    )

    for source, destination, weight in kruskal_result:

        print(
            f"{source} -> {destination} = {weight} m"
        )

    print(
        f"Total MST Weight: {kruskal_weight} meters"
    )

    print("\n" + "=" * 65)
    print("ALL GRAPH ALGORITHMS TESTED")
    print("=" * 65)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":
    test_graph_algorithms()