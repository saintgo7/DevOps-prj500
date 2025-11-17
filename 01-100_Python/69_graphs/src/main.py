"""
Program 69: Graphs - Graph Representation (Adjacency List & Matrix)
Demonstrates graph data structure with various representations
"""

from collections import defaultdict, deque


class GraphAdjacencyList:
    """Graph using adjacency list representation"""

    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed

    # Time Complexity: O(1)
    def add_edge(self, u, v, weight=1):
        """Add edge from u to v"""
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))

    # Time Complexity: O(V)
    def remove_edge(self, u, v):
        """Remove edge from u to v"""
        self.graph[u] = [(node, w) for node, w in self.graph[u] if node != v]
        if not self.directed:
            self.graph[v] = [(node, w) for node, w in self.graph[v] if node != u]

    def add_vertex(self, v):
        """Add vertex"""
        if v not in self.graph:
            self.graph[v] = []

    def get_vertices(self):
        """Get all vertices"""
        return list(self.graph.keys())

    def get_edges(self):
        """Get all edges"""
        edges = []
        for u in self.graph:
            for v, w in self.graph[u]:
                if self.directed or u <= v:
                    edges.append((u, v, w))
        return edges

    def get_neighbors(self, v):
        """Get neighbors of vertex v"""
        return self.graph[v]

    def has_edge(self, u, v):
        """Check if edge exists"""
        return any(node == v for node, _ in self.graph[u])

    def degree(self, v):
        """Get degree of vertex"""
        if self.directed:
            out_degree = len(self.graph[v])
            in_degree = sum(1 for u in self.graph for node, _ in self.graph[u] if node == v)
            return out_degree, in_degree
        return len(self.graph[v])

    def display(self):
        """Display graph"""
        print(f"Graph ({'Directed' if self.directed else 'Undirected'}):")
        for vertex in sorted(self.graph.keys()):
            neighbors = ', '.join(f"{v}({w})" for v, w in self.graph[vertex])
            print(f"  {vertex} -> {neighbors if neighbors else 'None'}")


class GraphAdjacencyMatrix:
    """Graph using adjacency matrix representation"""

    def __init__(self, num_vertices, directed=False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]
        self.vertex_map = {}  # Map vertex name to index
        self.reverse_map = {}  # Map index to vertex name
        self.next_index = 0

    def _get_index(self, vertex):
        """Get or create index for vertex"""
        if vertex not in self.vertex_map:
            if self.next_index >= self.num_vertices:
                raise ValueError("Too many vertices")
            self.vertex_map[vertex] = self.next_index
            self.reverse_map[self.next_index] = vertex
            self.next_index += 1
        return self.vertex_map[vertex]

    # Time Complexity: O(1)
    def add_edge(self, u, v, weight=1):
        """Add edge from u to v"""
        u_idx = self._get_index(u)
        v_idx = self._get_index(v)

        self.matrix[u_idx][v_idx] = weight
        if not self.directed:
            self.matrix[v_idx][u_idx] = weight

    def remove_edge(self, u, v):
        """Remove edge from u to v"""
        if u in self.vertex_map and v in self.vertex_map:
            u_idx = self.vertex_map[u]
            v_idx = self.vertex_map[v]

            self.matrix[u_idx][v_idx] = 0
            if not self.directed:
                self.matrix[v_idx][u_idx] = 0

    def has_edge(self, u, v):
        """Check if edge exists"""
        if u in self.vertex_map and v in self.vertex_map:
            u_idx = self.vertex_map[u]
            v_idx = self.vertex_map[v]
            return self.matrix[u_idx][v_idx] != 0
        return False

    def get_neighbors(self, vertex):
        """Get neighbors of vertex"""
        if vertex not in self.vertex_map:
            return []

        v_idx = self.vertex_map[vertex]
        neighbors = []

        for i in range(self.num_vertices):
            if self.matrix[v_idx][i] != 0:
                neighbors.append((self.reverse_map[i], self.matrix[v_idx][i]))

        return neighbors

    def display(self):
        """Display adjacency matrix"""
        print(f"\nAdjacency Matrix ({'Directed' if self.directed else 'Undirected'}):")

        # Header
        vertices = [self.reverse_map[i] for i in range(self.next_index)]
        print("    ", end="")
        for v in vertices:
            print(f"{v:4}", end="")
        print()

        # Matrix
        for i in range(self.next_index):
            print(f"{self.reverse_map[i]:4}", end="")
            for j in range(self.next_index):
                print(f"{self.matrix[i][j]:4}", end="")
            print()


class WeightedGraph:
    """Weighted graph implementation"""

    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed

    def add_edge(self, u, v, weight):
        """Add weighted edge"""
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))

    def display(self):
        """Display weighted graph"""
        print(f"\nWeighted Graph ({'Directed' if self.directed else 'Undirected'}):")
        for vertex in sorted(self.graph.keys()):
            edges = ', '.join(f"{v}(w={w})" for v, w in self.graph[vertex])
            print(f"  {vertex} -> {edges}")


def graph_properties():
    """Demonstrate various graph properties"""

    print("\n=== Graph Properties ===\n")

    def is_connected(graph):
        """Check if undirected graph is connected - Time: O(V+E)"""
        if not graph.graph:
            return True

        visited = set()
        start = next(iter(graph.graph))

        def dfs(v):
            visited.add(v)
            for neighbor, _ in graph.graph[v]:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(start)
        return len(visited) == len(graph.graph)

    def has_cycle_undirected(graph):
        """Detect cycle in undirected graph - Time: O(V+E)"""
        visited = set()

        def dfs(v, parent):
            visited.add(v)

            for neighbor, _ in graph.graph[v]:
                if neighbor not in visited:
                    if dfs(neighbor, v):
                        return True
                elif neighbor != parent:
                    return True

            return False

        for vertex in graph.graph:
            if vertex not in visited:
                if dfs(vertex, None):
                    return True

        return False

    def has_cycle_directed(graph):
        """Detect cycle in directed graph - Time: O(V+E)"""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {v: WHITE for v in graph.graph}

        def dfs(v):
            color[v] = GRAY

            for neighbor, _ in graph.graph[v]:
                if color.get(neighbor, WHITE) == GRAY:
                    return True
                if color.get(neighbor, WHITE) == WHITE:
                    if dfs(neighbor):
                        return True

            color[v] = BLACK
            return False

        for vertex in graph.graph:
            if color[vertex] == WHITE:
                if dfs(vertex):
                    return True

        return False

    # Undirected graph
    g1 = GraphAdjacencyList(directed=False)
    edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
    for u, v in edges:
        g1.add_edge(u, v)

    print("Undirected Graph:")
    g1.display()
    print(f"\nIs connected: {is_connected(g1)}")
    print(f"Has cycle: {has_cycle_undirected(g1)}")

    # Directed graph
    g2 = GraphAdjacencyList(directed=True)
    edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
    for u, v in edges:
        g2.add_edge(u, v)

    print("\n\nDirected Graph:")
    g2.display()
    print(f"\nHas cycle: {has_cycle_directed(g2)}")


def graph_coloring():
    """Demonstrate graph coloring problem"""

    print("\n=== Graph Coloring ===\n")

    def color_graph(graph, num_colors):
        """Color graph using greedy approach - Time: O(V^2)"""
        vertices = list(graph.graph.keys())
        color_map = {}

        for vertex in vertices:
            # Get colors of neighbors
            neighbor_colors = set()
            for neighbor, _ in graph.graph[vertex]:
                if neighbor in color_map:
                    neighbor_colors.add(color_map[neighbor])

            # Assign first available color
            for color in range(num_colors):
                if color not in neighbor_colors:
                    color_map[vertex] = color
                    break

        return color_map

    # Create graph
    g = GraphAdjacencyList(directed=False)
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4)]
    for u, v in edges:
        g.add_edge(u, v)

    print("Graph:")
    g.display()

    colors = color_graph(g, 3)
    print("\nGraph Coloring (3 colors):")
    for vertex, color in sorted(colors.items()):
        print(f"  Vertex {vertex}: Color {color}")


def bipartite_check():
    """Check if graph is bipartite"""

    print("\n=== Bipartite Graph Check ===\n")

    def is_bipartite(graph):
        """Check if graph is bipartite using BFS - Time: O(V+E)"""
        color = {}

        for start in graph.graph:
            if start in color:
                continue

            queue = deque([start])
            color[start] = 0

            while queue:
                v = queue.popleft()

                for neighbor, _ in graph.graph[v]:
                    if neighbor not in color:
                        color[neighbor] = 1 - color[v]
                        queue.append(neighbor)
                    elif color[neighbor] == color[v]:
                        return False, None

        return True, color

    # Bipartite graph
    g1 = GraphAdjacencyList(directed=False)
    edges = [(0, 1), (0, 3), (1, 2), (2, 3)]
    for u, v in edges:
        g1.add_edge(u, v)

    print("Graph 1:")
    g1.display()

    is_bip, coloring = is_bipartite(g1)
    print(f"\nIs bipartite: {is_bip}")
    if is_bip:
        print("Two sets:")
        set0 = [v for v, c in coloring.items() if c == 0]
        set1 = [v for v, c in coloring.items() if c == 1]
        print(f"  Set 0: {set0}")
        print(f"  Set 1: {set1}")

    # Non-bipartite graph
    g2 = GraphAdjacencyList(directed=False)
    edges = [(0, 1), (1, 2), (2, 0)]
    for u, v in edges:
        g2.add_edge(u, v)

    print("\n\nGraph 2:")
    g2.display()

    is_bip, _ = is_bipartite(g2)
    print(f"\nIs bipartite: {is_bip}")


def transpose_graph():
    """Get transpose of directed graph"""

    print("\n=== Graph Transpose ===\n")

    def get_transpose(graph):
        """Get transpose (reverse all edges) - Time: O(V+E)"""
        transposed = GraphAdjacencyList(directed=True)

        for u in graph.graph:
            for v, w in graph.graph[u]:
                transposed.add_edge(v, u, w)

        return transposed

    g = GraphAdjacencyList(directed=True)
    edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
    for u, v in edges:
        g.add_edge(u, v)

    print("Original Graph:")
    g.display()

    transposed = get_transpose(g)
    print("\n\nTransposed Graph:")
    transposed.display()


def main():
    """Main function to demonstrate graph operations"""

    print("=" * 60)
    print("PROGRAM 69: GRAPHS - REPRESENTATION")
    print("=" * 60)

    # Adjacency List - Undirected
    print("\n=== Adjacency List - Undirected Graph ===\n")

    g1 = GraphAdjacencyList(directed=False)

    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4)]
    print(f"Adding edges: {edges}")

    for u, v in edges:
        g1.add_edge(u, v)

    g1.display()

    print(f"\nVertices: {g1.get_vertices()}")
    print(f"Edges: {g1.get_edges()}")
    print(f"Neighbors of 1: {g1.get_neighbors(1)}")
    print(f"Degree of 3: {g1.degree(3)}")
    print(f"Has edge (1, 3): {g1.has_edge(1, 3)}")
    print(f"Has edge (1, 4): {g1.has_edge(1, 4)}")

    print("\n" + "-" * 60)

    # Adjacency List - Directed
    print("\n=== Adjacency List - Directed Graph ===\n")

    g2 = GraphAdjacencyList(directed=True)

    edges = [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 3)]
    print(f"Adding edges: {edges}")

    for u, v in edges:
        g2.add_edge(u, v)

    g2.display()

    print(f"\nDegree of 2 (out, in): {g2.degree(2)}")

    print("\n" + "-" * 60)

    # Adjacency Matrix
    print("\n=== Adjacency Matrix - Undirected Graph ===\n")

    g3 = GraphAdjacencyMatrix(5, directed=False)

    edges = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
    print(f"Adding edges: {edges}")

    for u, v in edges:
        g3.add_edge(u, v)

    g3.display()

    print(f"\nNeighbors of B: {g3.get_neighbors('B')}")
    print(f"Has edge (A, D): {g3.has_edge('A', 'D')}")

    print("\n" + "-" * 60)

    # Weighted Graph
    print("\n=== Weighted Graph ===\n")

    wg = WeightedGraph(directed=False)

    edges = [('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1),
             ('B', 'D', 5), ('C', 'D', 8), ('C', 'E', 10), ('D', 'E', 2)]

    print("Adding weighted edges:")
    for u, v, w in edges:
        wg.add_edge(u, v, w)
        print(f"  {u} -- {v} (weight: {w})")

    wg.display()

    print("\n" + "-" * 60)

    # Graph Properties
    graph_properties()

    print("\n" + "-" * 60)

    # Graph Coloring
    graph_coloring()

    print("\n" + "-" * 60)

    # Bipartite Check
    bipartite_check()

    print("\n" + "-" * 60)

    # Transpose
    transpose_graph()

    print("\n" + "=" * 60)
    print("Graph operations demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
