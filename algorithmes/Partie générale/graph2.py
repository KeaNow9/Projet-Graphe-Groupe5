from collections import defaultdict
import math

class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.edges = []
        self.directed = directed

    def add_edge(self, u, v, w=1):
        self.graph[u].append((v, w))
        self.edges.append((w, u, v))
        if not self.directed:
            self.graph[v].append((u, w))
            self.edges.append((w, v, u))

    def get_nodes(self):
        return list(self.graph.keys())

    def display(self):
        for node, neighbors in self.graph.items():
            print(f"{node} -> {neighbors}")

    # ----------------------
    # BFS
    # ----------------------
    def bfs(self, start):
        visited = set()
        queue = [start]  # liste normale utilisée comme file
        order = []

        while queue:
            node = queue.pop(0)  # retire le premier élément
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor, _ in self.graph[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        return order

    # ----------------------
    # DFS
    # ----------------------
    def dfs(self, start):
        visited = set()
        order = []

        def explore(node):
            visited.add(node)
            order.append(node)
            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    explore(neighbor)

        explore(start)
        return order

    # ----------------------
    # Kruskal
    # ----------------------
    def kruskal(self):
        if self.directed:
            raise ValueError("Kruskal ne peut être utilisé que sur un graphe non orienté !")

        parent = {}
        rank = {}

        def find(n):
            if parent[n] != n:
                parent[n] = find(parent[n])
            return parent[n]

        def union(n1, n2):
            r1, r2 = find(n1), find(n2)
            if r1 != r2:
                if rank[r1] < rank[r2]:
                    parent[r1] = r2
                elif rank[r1] > rank[r2]:
                    parent[r2] = r1
                else:
                    parent[r2] = r1
                    rank[r1] += 1

        for node in self.graph:
            parent[node] = node
            rank[node] = 0

        mst = []
        total_cost = 0
        for w, u, v in sorted(self.edges):
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, w))
                total_cost += w

        return mst, total_cost

    # ----------------------
    # Prim
    # ----------------------
    def prim(self, start):
        if self.directed:
            raise ValueError("Prim ne peut être utilisé que sur un graphe non orienté !")

        visited = set([start])
        edges = [(w, start, v) for v, w in self.graph[start]]
        mst = []
        total_cost = 0

        while edges:
            # trouve l'arête de poids minimal
            min_index = 0
            for i in range(len(edges)):
                if edges[i][0] < edges[min_index][0]:
                    min_index = i
            w, u, v = edges.pop(min_index)

            if v not in visited:
                visited.add(v)
                mst.append((u, v, w))
                total_cost += w
                for to, weight in self.graph[v]:
                    if to not in visited:
                        edges.append((weight, v, to))

        return mst, total_cost

    # ----------------------
    # Dijkstra
    # ----------------------
    def dijkstra(self, start):
        dist = {node: math.inf for node in self.graph}
        dist[start] = 0
        pq = [(0, start)]  # liste simple

        while pq:
            # chercher le sommet avec la plus petite distance
            min_index = 0
            for i in range(len(pq)):
                if pq[i][0] < pq[min_index][0]:
                    min_index = i
            d, node = pq.pop(min_index)

            for neighbor, w in self.graph[node]:
                new_d = d + w
                if new_d < dist[neighbor]:
                    dist[neighbor] = new_d
                    pq.append((new_d, neighbor))

        return dist

    # ----------------------
    # Bellman-Ford
    # ----------------------
    def bellman_ford(self, start):
        dist = {node: math.inf for node in self.graph}
        dist[start] = 0

        for _ in range(len(self.graph) - 1):
            for w, u, v in self.edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w

        for w, u, v in self.edges:
            if dist[u] + w < dist[v]:
                print("Cycle négatif détecté !")
                return None
        return dist

    # ----------------------
    # Floyd-Warshall
    # ----------------------
    def floyd_warshall(self):
        nodes = list(self.graph.keys())
        dist = {i: {j: math.inf for j in nodes} for i in nodes}

        for node in nodes:
            dist[node][node] = 0
            for neighbor, w in self.graph[node]:
                dist[node][neighbor] = w

        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist

    # --------------------------------------------------------
    # Exemple d’utilisation
    # --------------------------------------------------------
if __name__ == "__main__":
        g = Graph(directed=False)

        # --- Arêtes d'après le schéma ---
        # Rennes
        g.add_edge("Rennes", "Nantes", 45)
        g.add_edge("Rennes", "Caen", 75)
        g.add_edge("Rennes", "Paris", 110)
        g.add_edge("Rennes", "Bordeaux", 130)

        # Nantes
        g.add_edge("Nantes", "Paris", 80)
        g.add_edge("Nantes", "Bordeaux", 90)

        # Bordeaux
        g.add_edge("Bordeaux", "Paris", 150)
        g.add_edge("Bordeaux", "Lyon", 100)

        # Caen
        g.add_edge("Caen", "Paris", 50)
        g.add_edge("Caen", "Lille", 65)

        # Paris
        g.add_edge("Paris", "Lille", 70)
        g.add_edge("Paris", "Dijon", 60)

        # Lille
        g.add_edge("Lille", "Dijon", 120)
        g.add_edge("Lille", "Nancy", 100)

        # Dijon
        g.add_edge("Dijon", "Nancy", 75)
        g.add_edge("Dijon", "Lyon", 70)
        g.add_edge("Dijon", "Grenoble", 75)

        # Lyon
        g.add_edge("Lyon", "Grenoble", 40)
        g.add_edge("Lyon", "Nancy", 90)

        # Nancy
        g.add_edge("Nancy", "Grenoble", 80)

        # --- Démonstrations identiques à ton exemple ---
        print("=== Parcours ===")
        print("BFS depuis Rennes :", g.bfs("Rennes"))
        print("DFS depuis Rennes :", g.dfs("Rennes"))

        print("\n=== Arbre couvrant minimal ===")
        mst_k, cost_k = g.kruskal()
        print("Kruskal :", mst_k, " | Coût total :", cost_k)

        mst_p, cost_p = g.prim("Rennes")
        print("Prim :", mst_p, " | Coût total :", cost_p)

        print("\n=== Plus courts chemins ===")
        print("Dijkstra (depuis Bordeaux) :", g.dijkstra("Bordeaux"))
        print("Bellman-Ford (depuis Bordeaux) :", g.bellman_ford("Bordeaux"))

        print("\n=== Floyd-Warshall ===")
        dist = g.floyd_warshall()
        for i in dist:
            print(i, dist[i])