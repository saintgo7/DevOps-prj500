"""
Program 77: Shortest Path - Dijkstra, Bellman-Ford, Floyd-Warshall
Demonstrates shortest path algorithms for weighted graphs
"""

import heapq
from collections import defaultdict


class WeightedGraph:
    """Weighted graph for shortest path algorithms"""

    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed
        self.vertices = set()

    def add_edge(self, u, v, weight):
        """Add weighted edge"""
        self.graph[u].append((v, weight))
        self.vertices.add(u)
        self.vertices.add(v)

        if not self.directed:
            self.graph[v].append((u, weight))

    def display(self):
        """Display graph"""
        print(f"Weighted Graph ({'Directed' if self.directed else 'Undirected'}):")
        for u in sorted(self.graph.keys()):
            edges = ', '.join(f"{v}(w={w})" for v, w in self.graph[u])
            print(f"  {u} -> {edges}")


def dijkstra_algorithm():
    """
    Dijkstra's Algorithm - Single source shortest path
    Time: O((V + E) log V), Space: O(V)
    Works for: Non-negative weights only
    """

    print("\n=== Dijkstra's Algorithm ===\n")

    def dijkstra(graph, start):
        """Find shortest paths from start to all vertices"""
        distances = {vertex: float('inf') for vertex in graph.vertices}
        distances[start] = 0
        previous = {vertex: None for vertex in graph.vertices}

        # Priority queue: (distance, vertex)
        pq = [(0, start)]
        visited = set()

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current in visited:
                continue

            visited.add(current)

            for neighbor, weight in graph.graph[current]:
                distance = current_dist + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))

        return distances, previous

    def get_path(previous, start, end):
        """Reconstruct path from start to end"""
        path = []
        current = end

        while current is not None:
            path.append(current)
            current = previous[current]

        return path[::-1] if path[0] == start else None

    # Create graph
    g = WeightedGraph(directed=False)
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('C', 'E', 10),
        ('D', 'E', 2),
        ('D', 'F', 6),
        ('E', 'F', 3),
    ]

    for u, v, w in edges:
        g.add_edge(u, v, w)

    g.display()

    # Run Dijkstra
    start = 'A'
    distances, previous = dijkstra(g, start)

    print(f"\nShortest distances from {start}:")
    for vertex in sorted(distances.keys()):
        if distances[vertex] != float('inf'):
            path = get_path(previous, start, vertex)
            print(f"  To {vertex}: {distances[vertex]} (Path: {' -> '.join(path)})")


def bellman_ford_algorithm():
    """
    Bellman-Ford Algorithm - Single source shortest path
    Time: O(VE), Space: O(V)
    Works for: Negative weights, detects negative cycles
    """

    print("\n=== Bellman-Ford Algorithm ===\n")

    def bellman_ford(graph, start):
        """Find shortest paths, returns None if negative cycle exists"""
        distances = {vertex: float('inf') for vertex in graph.vertices}
        distances[start] = 0
        previous = {vertex: None for vertex in graph.vertices}

        # Relax edges V-1 times
        vertices_list = list(graph.vertices)
        for _ in range(len(vertices_list) - 1):
            for u in graph.graph:
                for v, weight in graph.graph[u]:
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        previous[v] = u

        # Check for negative cycles
        for u in graph.graph:
            for v, weight in graph.graph[u]:
                if distances[u] + weight < distances[v]:
                    return None, None  # Negative cycle detected

        return distances, previous

    # Create graph with negative weights
    g = WeightedGraph(directed=True)
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', -3),
        ('B', 'D', 2),
        ('C', 'D', 4),
        ('D', 'B', 1),
    ]

    for u, v, w in edges:
        g.add_edge(u, v, w)

    g.display()

    # Run Bellman-Ford
    start = 'A'
    result = bellman_ford(g, start)

    if result[0] is None:
        print("\nNegative cycle detected!")
    else:
        distances, previous = result
        print(f"\nShortest distances from {start}:")
        for vertex in sorted(distances.keys()):
            if distances[vertex] != float('inf'):
                print(f"  To {vertex}: {distances[vertex]}")


def floyd_warshall_algorithm():
    """
    Floyd-Warshall Algorithm - All pairs shortest paths
    Time: O(V³), Space: O(V²)
    Works for: Negative weights, finds all pairs
    """

    print("\n=== Floyd-Warshall Algorithm ===\n")

    def floyd_warshall(vertices, edges):
        """Find shortest paths between all pairs"""
        # Initialize distance matrix
        dist = {v: {u: float('inf') for u in vertices} for v in vertices}

        # Distance from vertex to itself is 0
        for v in vertices:
            dist[v][v] = 0

        # Add edge weights
        for u, v, w in edges:
            dist[u][v] = w

        # Floyd-Warshall algorithm
        for k in vertices:
            for i in vertices:
                for j in vertices:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist

    # Create graph
    vertices = ['A', 'B', 'C', 'D']
    edges = [
        ('A', 'B', 3),
        ('A', 'C', 8),
        ('A', 'D', -4),
        ('B', 'D', 7),
        ('B', 'C', 2),
        ('D', 'B', 5),
        ('D', 'C', 1),
    ]

    print("Graph edges:")
    for u, v, w in edges:
        print(f"  {u} -> {v} (weight: {w})")

    # Run Floyd-Warshall
    dist = floyd_warshall(vertices, edges)

    print("\nShortest distances (all pairs):")
    print("     ", end="")
    for v in sorted(vertices):
        print(f"{v:>6}", end="")
    print()

    for u in sorted(vertices):
        print(f"{u:>4} ", end="")
        for v in sorted(vertices):
            d = dist[u][v]
            if d == float('inf'):
                print(f"{'∞':>6}", end="")
            else:
                print(f"{d:>6}", end="")
        print()


def a_star_algorithm():
    """
    A* Algorithm - Heuristic-based shortest path
    Time: O(E), Space: O(V)
    """

    print("\n=== A* Algorithm ===\n")

    def heuristic(node, goal, positions):
        """Euclidean distance heuristic"""
        x1, y1 = positions[node]
        x2, y2 = positions[goal]
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def a_star(graph, start, goal, positions):
        """Find shortest path using A*"""
        open_set = [(0, start)]
        came_from = {}
        g_score = {vertex: float('inf') for vertex in graph.vertices}
        g_score[start] = 0
        f_score = {vertex: float('inf') for vertex in graph.vertices}
        f_score[start] = heuristic(start, goal, positions)

        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1], g_score[goal]

            for neighbor, weight in graph.graph[current]:
                tentative_g = g_score[current] + weight

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal, positions)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None, float('inf')

    # Create graph with positions
    g = WeightedGraph(directed=False)
    edges = [
        ('A', 'B', 1),
        ('A', 'C', 4),
        ('B', 'C', 2),
        ('B', 'D', 5),
        ('C', 'D', 1),
        ('D', 'E', 3),
    ]

    for u, v, w in edges:
        g.add_edge(u, v, w)

    # Node positions (for heuristic)
    positions = {
        'A': (0, 0),
        'B': (1, 0),
        'C': (0, 1),
        'D': (1, 1),
        'E': (2, 1),
    }

    print("Graph with positions:")
    for vertex in sorted(positions.keys()):
        x, y = positions[vertex]
        print(f"  {vertex}: ({x}, {y})")

    # Run A*
    start, goal = 'A', 'E'
    path, distance = a_star(g, start, goal, positions)

    print(f"\nPath from {start} to {goal}: {' -> '.join(path)}")
    print(f"Distance: {distance}")


def johnson_algorithm():
    """
    Johnson's Algorithm - All pairs shortest path
    Time: O(V²log V + VE), Space: O(V²)
    Efficient for sparse graphs
    """

    print("\n=== Johnson's Algorithm ===\n")

    def johnson(vertices, edges):
        """Find shortest paths using Johnson's algorithm"""
        # Add new vertex q
        augmented_edges = edges + [('q', v, 0) for v in vertices]
        augmented_vertices = vertices + ['q']

        # Run Bellman-Ford from q
        distances_from_q = {v: float('inf') for v in augmented_vertices}
        distances_from_q['q'] = 0

        for _ in range(len(augmented_vertices) - 1):
            for u, v, w in augmented_edges:
                if distances_from_q[u] + w < distances_from_q[v]:
                    distances_from_q[v] = distances_from_q[u] + w

        # Reweight edges
        reweighted_edges = []
        for u, v, w in edges:
            new_weight = w + distances_from_q[u] - distances_from_q[v]
            reweighted_edges.append((u, v, new_weight))

        # Run Dijkstra from each vertex
        result = {}
        for source in vertices:
            # Create graph for this source
            g = WeightedGraph(directed=True)
            for u, v, w in reweighted_edges:
                g.add_edge(u, v, w)

            # Run Dijkstra
            from_source = {v: float('inf') for v in vertices}
            from_source[source] = 0
            pq = [(0, source)]

            while pq:
                d, u = heapq.heappop(pq)
                if d > from_source[u]:
                    continue

                for v, w in g.graph[u]:
                    if from_source[u] + w < from_source[v]:
                        from_source[v] = from_source[u] + w
                        heapq.heappush(pq, (from_source[v], v))

            # Adjust distances back
            result[source] = {}
            for target in vertices:
                if from_source[target] != float('inf'):
                    result[source][target] = from_source[target] + \
                                            distances_from_q[target] - distances_from_q[source]
                else:
                    result[source][target] = float('inf')

        return result

    vertices = ['A', 'B', 'C', 'D']
    edges = [
        ('A', 'B', 3),
        ('A', 'C', 8),
        ('B', 'D', 7),
        ('B', 'C', 2),
        ('D', 'A', -5),
        ('D', 'C', 1),
    ]

    print("Graph edges:")
    for u, v, w in edges:
        print(f"  {u} -> {v} (weight: {w})")

    dist = johnson(vertices, edges)

    print("\nShortest distances (Johnson's):")
    print("     ", end="")
    for v in sorted(vertices):
        print(f"{v:>6}", end="")
    print()

    for u in sorted(vertices):
        print(f"{u:>4} ", end="")
        for v in sorted(vertices):
            d = dist[u][v]
            if d == float('inf'):
                print(f"{'∞':>6}", end="")
            else:
                print(f"{d:>6}", end="")
        print()


def shortest_path_dag():
    """
    Shortest path in DAG using topological sort
    Time: O(V + E), Space: O(V)
    """

    print("\n=== Shortest Path in DAG ===\n")

    def topological_sort(graph):
        """Topological sort using DFS"""
        visited = set()
        stack = []

        def dfs(v):
            visited.add(v)
            for neighbor, _ in graph.graph[v]:
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(v)

        for vertex in graph.vertices:
            if vertex not in visited:
                dfs(vertex)

        return stack[::-1]

    def shortest_path_dag_topo(graph, start):
        """Find shortest paths in DAG"""
        topo_order = topological_sort(graph)
        distances = {v: float('inf') for v in graph.vertices}
        distances[start] = 0

        for u in topo_order:
            if distances[u] != float('inf'):
                for v, weight in graph.graph[u]:
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight

        return distances

    # Create DAG
    g = WeightedGraph(directed=True)
    edges = [
        ('A', 'B', 3),
        ('A', 'C', 6),
        ('B', 'C', 4),
        ('B', 'D', 5),
        ('B', 'E', 8),
        ('C', 'D', 2),
        ('D', 'E', 1),
    ]

    for u, v, w in edges:
        g.add_edge(u, v, w)

    g.display()

    start = 'A'
    distances = shortest_path_dag_topo(g, start)

    print(f"\nShortest distances from {start} (DAG):")
    for vertex in sorted(distances.keys()):
        d = distances[vertex]
        if d != float('inf'):
            print(f"  To {vertex}: {d}")


def main():
    """Main function to demonstrate shortest path algorithms"""

    print("=" * 60)
    print("PROGRAM 77: SHORTEST PATH ALGORITHMS")
    print("=" * 60)

    # Dijkstra's Algorithm
    dijkstra_algorithm()

    print("\n" + "=" * 60)

    # Bellman-Ford Algorithm
    bellman_ford_algorithm()

    print("\n" + "=" * 60)

    # Floyd-Warshall Algorithm
    floyd_warshall_algorithm()

    print("\n" + "=" * 60)

    # A* Algorithm
    a_star_algorithm()

    print("\n" + "=" * 60)

    # Johnson's Algorithm
    johnson_algorithm()

    print("\n" + "=" * 60)

    # Shortest Path in DAG
    shortest_path_dag()

    print("\n" + "=" * 60)
    print("Shortest path algorithms demonstration completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
