"""
Program 76: Graph Traversal - BFS, DFS, Topological Sort
Demonstrates graph traversal algorithms
"""

from collections import defaultdict, deque


class Graph:
    """Graph class for traversal demonstrations"""

    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed

    def add_edge(self, u, v):
        """Add edge to graph"""
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)

    def get_vertices(self):
        """Get all vertices"""
        vertices = set()
        for u in self.graph:
            vertices.add(u)
            for v in self.graph[u]:
                vertices.add(v)
        return list(vertices)


def bfs_traversal():
    """
    Breadth-First Search (BFS)
    Time: O(V + E), Space: O(V)
    """

    print("\n=== Breadth-First Search (BFS) ===\n")

    def bfs(graph, start):
        """BFS traversal from start vertex"""
        visited = set()
        queue = deque([start])
        visited.add(start)
        result = []

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def bfs_levels(graph, start):
        """BFS with level tracking"""
        visited = {start: 0}
        queue = deque([start])
        levels = defaultdict(list)

        while queue:
            vertex = queue.popleft()
            level = visited[vertex]
            levels[level].append(vertex)

            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    visited[neighbor] = level + 1
                    queue.append(neighbor)

        return levels

    def shortest_path_bfs(graph, start, end):
        """Find shortest path using BFS"""
        if start == end:
            return [start]

        visited = {start}
        queue = deque([(start, [start])])

        while queue:
            vertex, path = queue.popleft()

            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]

                    if neighbor == end:
                        return new_path

                    queue.append((neighbor, new_path))

        return None

    # Create graph
    g = Graph()
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5)]

    for u, v in edges:
        g.add_edge(u, v)

    print("Graph edges:")
    for u in sorted(g.graph.keys()):
        print(f"  {u} -> {g.graph[u]}")

    # BFS traversal
    start = 0
    traversal = bfs(g, start)
    print(f"\nBFS from {start}: {traversal}")

    # BFS with levels
    levels = bfs_levels(g, start)
    print("\nBFS Levels:")
    for level in sorted(levels.keys()):
        print(f"  Level {level}: {levels[level]}")

    # Shortest path
    end = 5
    path = shortest_path_bfs(g, start, end)
    print(f"\nShortest path from {start} to {end}: {path}")


def dfs_traversal():
    """
    Depth-First Search (DFS)
    Time: O(V + E), Space: O(V)
    """

    print("\n=== Depth-First Search (DFS) ===\n")

    def dfs_recursive(graph, start, visited=None, result=None):
        """DFS using recursion"""
        if visited is None:
            visited = set()
        if result is None:
            result = []

        visited.add(start)
        result.append(start)

        for neighbor in graph.graph[start]:
            if neighbor not in visited:
                dfs_recursive(graph, neighbor, visited, result)

        return result

    def dfs_iterative(graph, start):
        """DFS using stack"""
        visited = set()
        stack = [start]
        result = []

        while stack:
            vertex = stack.pop()

            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                # Add neighbors in reverse order for same order as recursive
                for neighbor in reversed(graph.graph[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return result

    def dfs_paths(graph, start, end, path=None):
        """Find all paths from start to end using DFS"""
        if path is None:
            path = []

        path = path + [start]

        if start == end:
            return [path]

        paths = []
        for neighbor in graph.graph[start]:
            if neighbor not in path:
                new_paths = dfs_paths(graph, neighbor, end, path)
                paths.extend(new_paths)

        return paths

    # Create graph
    g = Graph()
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5)]

    for u, v in edges:
        g.add_edge(u, v)

    print("Graph edges:")
    for u in sorted(g.graph.keys()):
        print(f"  {u} -> {g.graph[u]}")

    # DFS traversals
    start = 0
    recursive = dfs_recursive(g, start)
    iterative = dfs_iterative(g, start)

    print(f"\nDFS Recursive from {start}: {recursive}")
    print(f"DFS Iterative from {start}: {iterative}")

    # All paths
    end = 5
    paths = dfs_paths(g, start, end)
    print(f"\nAll paths from {start} to {end}:")
    for path in paths:
        print(f"  {' -> '.join(map(str, path))}")


def topological_sort():
    """
    Topological Sort - Linear ordering of vertices in DAG
    Time: O(V + E), Space: O(V)
    """

    print("\n=== Topological Sort ===\n")

    def topological_sort_dfs(graph):
        """Topological sort using DFS"""
        visited = set()
        stack = []

        def dfs(vertex):
            visited.add(vertex)

            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor)

            stack.append(vertex)

        for vertex in graph.graph:
            if vertex not in visited:
                dfs(vertex)

        return stack[::-1]

    def topological_sort_bfs(graph):
        """Topological sort using BFS (Kahn's algorithm)"""
        # Calculate in-degrees
        in_degree = defaultdict(int)
        for u in graph.graph:
            for v in graph.graph[u]:
                in_degree[v] += 1

        # Find vertices with in-degree 0
        queue = deque([v for v in graph.graph if in_degree[v] == 0])
        result = []

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor in graph.graph[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result

    # Create DAG (Directed Acyclic Graph)
    g = Graph(directed=True)
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]

    for u, v in edges:
        g.add_edge(u, v)

    print("DAG edges:")
    for u in sorted(g.graph.keys()):
        print(f"  {u} -> {g.graph[u]}")

    # Topological sorts
    topo_dfs = topological_sort_dfs(g)
    topo_bfs = topological_sort_bfs(g)

    print(f"\nTopological Sort (DFS): {topo_dfs}")
    print(f"Topological Sort (BFS): {topo_bfs}")


def detect_cycle():
    """Detect cycles in graphs"""

    print("\n=== Cycle Detection ===\n")

    def has_cycle_undirected(graph):
        """Detect cycle in undirected graph using DFS"""
        visited = set()

        def dfs(vertex, parent):
            visited.add(vertex)

            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    if dfs(neighbor, vertex):
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
        """Detect cycle in directed graph using DFS"""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {v: WHITE for v in graph.graph}

        def dfs(vertex):
            color[vertex] = GRAY

            for neighbor in graph.graph[vertex]:
                if color.get(neighbor, WHITE) == GRAY:
                    return True
                if color.get(neighbor, WHITE) == WHITE:
                    if dfs(neighbor):
                        return True

            color[vertex] = BLACK
            return False

        for vertex in graph.graph:
            if color[vertex] == WHITE:
                if dfs(vertex):
                    return True

        return False

    # Undirected graph with cycle
    g1 = Graph(directed=False)
    edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
    for u, v in edges:
        g1.add_edge(u, v)

    print("Undirected Graph:")
    for u in sorted(g1.graph.keys()):
        print(f"  {u} -- {g1.graph[u]}")
    print(f"Has cycle: {has_cycle_undirected(g1)}")

    # Directed graph with cycle
    g2 = Graph(directed=True)
    edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
    for u, v in edges:
        g2.add_edge(u, v)

    print("\nDirected Graph:")
    for u in sorted(g2.graph.keys()):
        print(f"  {u} -> {g2.graph[u]}")
    print(f"Has cycle: {has_cycle_directed(g2)}")


def connected_components():
    """Find connected components in graph"""

    print("\n=== Connected Components ===\n")

    def find_components(graph):
        """Find all connected components using DFS"""
        visited = set()
        components = []

        def dfs(vertex, component):
            visited.add(vertex)
            component.append(vertex)

            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor, component)

        for vertex in graph.graph:
            if vertex not in visited:
                component = []
                dfs(vertex, component)
                components.append(sorted(component))

        return components

    # Graph with multiple components
    g = Graph(directed=False)
    edges = [(0, 1), (1, 2), (3, 4), (5, 6), (6, 7), (7, 5)]

    for u, v in edges:
        g.add_edge(u, v)

    print("Graph edges:")
    for u in sorted(g.graph.keys()):
        print(f"  {u} -- {g.graph[u]}")

    components = find_components(g)

    print(f"\nNumber of components: {len(components)}")
    for i, comp in enumerate(components, 1):
        print(f"  Component {i}: {comp}")


def bipartite_check():
    """Check if graph is bipartite using BFS"""

    print("\n=== Bipartite Graph Check ===\n")

    def is_bipartite(graph):
        """Check if graph is bipartite using BFS coloring"""
        color = {}

        for start in graph.graph:
            if start in color:
                continue

            queue = deque([start])
            color[start] = 0

            while queue:
                vertex = queue.popleft()

                for neighbor in graph.graph[vertex]:
                    if neighbor not in color:
                        color[neighbor] = 1 - color[vertex]
                        queue.append(neighbor)
                    elif color[neighbor] == color[vertex]:
                        return False, None

        return True, color

    # Bipartite graph
    g1 = Graph(directed=False)
    edges = [(0, 1), (0, 3), (1, 2), (2, 3)]
    for u, v in edges:
        g1.add_edge(u, v)

    print("Graph 1:")
    for u in sorted(g1.graph.keys()):
        print(f"  {u} -- {g1.graph[u]}")

    is_bip, coloring = is_bipartite(g1)
    print(f"Is bipartite: {is_bip}")

    if is_bip:
        set0 = [v for v, c in coloring.items() if c == 0]
        set1 = [v for v, c in coloring.items() if c == 1]
        print(f"  Set 0: {sorted(set0)}")
        print(f"  Set 1: {sorted(set1)}")


def articulation_points():
    """Find articulation points (cut vertices) in graph"""

    print("\n=== Articulation Points ===\n")

    def find_articulation_points(graph):
        """Find articulation points using Tarjan's algorithm"""
        visited = set()
        disc = {}
        low = {}
        parent = {}
        ap = set()
        time = [0]

        def dfs(u):
            children = 0
            visited.add(u)
            disc[u] = low[u] = time[0]
            time[0] += 1

            for v in graph.graph[u]:
                if v not in visited:
                    children += 1
                    parent[v] = u
                    dfs(v)

                    low[u] = min(low[u], low[v])

                    # u is articulation point if:
                    # 1. u is root with more than 1 child
                    # 2. u is not root and low[v] >= disc[u]
                    if parent.get(u) is None and children > 1:
                        ap.add(u)
                    if parent.get(u) is not None and low[v] >= disc[u]:
                        ap.add(u)

                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])

        for vertex in graph.graph:
            if vertex not in visited:
                dfs(vertex)

        return list(ap)

    # Graph with articulation points
    g = Graph(directed=False)
    edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)]

    for u, v in edges:
        g.add_edge(u, v)

    print("Graph edges:")
    for u in sorted(g.graph.keys()):
        print(f"  {u} -- {g.graph[u]}")

    ap = find_articulation_points(g)
    print(f"\nArticulation points: {sorted(ap)}")


def main():
    """Main function to demonstrate graph traversal"""

    print("=" * 60)
    print("PROGRAM 76: GRAPH TRAVERSAL")
    print("=" * 60)

    # BFS
    bfs_traversal()

    print("\n" + "=" * 60)

    # DFS
    dfs_traversal()

    print("\n" + "=" * 60)

    # Topological Sort
    topological_sort()

    print("\n" + "=" * 60)

    # Cycle Detection
    detect_cycle()

    print("\n" + "=" * 60)

    # Connected Components
    connected_components()

    print("\n" + "=" * 60)

    # Bipartite Check
    bipartite_check()

    print("\n" + "=" * 60)

    # Articulation Points
    articulation_points()

    print("\n" + "=" * 60)
    print("Graph traversal demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
